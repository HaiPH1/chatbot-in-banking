from flask import Flask
from flask import session
from flask import render_template, jsonify, request
import requests
import random
import json
import re
import os
from flask_session import Session
import response_config
import datetime
from utils import normalize_text


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
sess = Session(app)


@app.route("/")
def hello_world():
    """
    Sample hello world
    """
    session["intent"] = None
    session["entity"] = None
    session["value"] = None
    session["card_id"] = None
    session["time_sequen"] = 0
    return render_template("home.html")


@app.route("/reset_session")
def reset_session():
    """
    reset session
    """
    session["intent"] = None
    session["entity"] = None
    session["value"] = None
    session["card_id"] = None
    session["time_sequen"] = 0
    return jsonify(
                {"status": "success"}
            )


def get_random_response(intent):
    return random.choice(response_config.default_responses[intent])


@app.route("/chat", methods=["POST"])
def chat():
    """
    chat end point that performs NLU using rasa.ai
    and constructs response from response.py
    """
    response_text = ""
    try:
        try:
            text = request.form["text"].lower()
        except Exception:
            text = eval(request.get_data())["text"].lower()

        text = normalize_text(text)

        try:
            responses = requests.request(
                "POST", "http://localhost:5005/model/parse",
                data=json.dumps({"text": text})
            )
        except Exception:
            return jsonify(
                    {
                        "status": "nlu_error",
                        "response": get_random_response("confused")
                    }
                )
        responses = responses.json()
        entities = responses["entities"]
        length = len(entities)
        confidence = responses["intent"]["confidence"]

        if confidence > 0.5:
            print(session.get("intent", "not set"), responses["intent"]["name"])
            if (
                responses["intent"]["name"] != session.get("intent", "not set")
                and not (
                    session.get("intent", "not set") == "lost_card"
                    and responses["intent"]["name"] == "thanks"
                )
            ):
                session["time_sequen"] = 0

                session["intent"] = responses["intent"]["name"]

        intent = session.get("intent", "not set")

        # print(intent)
        if intent is None:
            response_text = get_random_response("greet")
        elif intent == "thanks":
            response_text = get_random_response('thanks')
        # Un-affirm
        elif intent == "un-affirm":
            response_text = get_random_response('goodbye')
        # New card
        elif intent == "new_card":
            entity, value = None, None
            ncard_res = response_config.new_card_response
            for card_ty in response_config.supported_cards:
                if card_ty in text:
                    entity = "card_type"
                    value = card_ty

            if text == "1" or "credit" in text or "1" in text.split():
                entity = "card_type"
                value = "thẻ credit"
            elif text == "2" or "atm" in text or "2" in text.split():
                entity = "card_type"
                value = "thẻ atm"

            if entity is None:
                time_sequen = session.get("time_sequen", "not set")
                if time_sequen == 1:
                    session["time_sequen"] = 0
                    session["intent"] = None
                    # intent = session.get('intent', 'not set')
                    response_text = ncard_res['new_card_reject']
                else:
                    session["time_sequen"] = 1
                    response_text = ncard_res['new_card_intro']

            else:
                session["time_sequen"] = 0
                response_text = ncard_res['new_card_info'].format(value)

        # Lost card
        elif intent == "lost_card":
            card_ids = re.findall(
                            r"\s\d{11}\s|\s\d{11}$|^\d{11}\s|^\d{11}$",
                            text
                        )

            if len(card_ids) > 0:
                card_id = card_ids[0].strip()
                session["card_id"] = card_id

            affirm_bool = False
            for aff in response_config.affirm_message:
                if aff in text.split():
                    affirm_bool = True

            card_id = session.get("card_id", "not set")
            time_sequen = session.get("time_sequen", "not set")
            if card_id is None:
                response_text = (
                    "Quý khách vui lòng cung cấp số thẻ "
                    "(số thẻ được in ở mặt sau của thẻ, bao gồm 11 chữ số): "
                )
            elif not affirm_bool:
                if time_sequen == 0:
                    response_text = (
                        "Chúng tôi sẽ thực hiện khóa thẻ {0} của quý khách."
                        " Quý khách chắc chắn chứ?".format(
                            card_id
                        )
                    )
                    session["time_sequen"] = 1
                else:
                    response_text = "Quý khách còn cần hỗ trợ gì nữa không?"
                    session["intent"] = None
                    session["time_sequen"] = 0
            else:
                response_text = "Chúng tôi đã khóa thẻ {0} của quý khách. "\
                                "Quý khách cần hỗ trợ gì nữa không ạ?".format(
                                                                        card_id
                                                                    )
                session["intent"] = None
                session["time_sequen"] = 0

        # Card charge
        elif intent == "card_charge":
            if length > 0 and entities[0]["entity"] == "card_type":
                if entities[0]["value"].lower() == "thẻ atm":
                    response_text = "Thẻ ATM sử dụng miễn phí hàng năm, "\
                                    "không cần nộp phí sử dụng."
                elif (entities[0]["value"].lower()
                        in response_config.supported_cards):
                    response_text = "Phí thường niên {0} là "\
                                    "300.000 vnđ/năm.".format(
                                                entities[0]["value"].lower()
                                            )
                else:
                    response_text = "Xin lỗi, quý khách có thể cung cấp tên"\
                                    " chính xác loại thẻ mình đang "\
                                    "dùng được không ạ?"

            else:
                card_charge = response_config.card_charge
                response_text = card_charge["card_charge_intro"]
                session["intent"] = None
                session["time_sequen"] = 0

        # Change Password
        elif intent == "change_password":
            response_text = "Quý khách không thể đổi mật khẩu trên chatbot. "\
                            "Vui lòng đến chi nhánh gần nhất của chúng "\
                            "tôi để được hỗ trợ."
            session["intent"] = None
            session["time_sequen"] = 0

        # Intro Loan
        elif intent == "loan":
            entity, value = None, None

            if (
                text == "1"
                or "số 1" in text
                or "gói 1" in text
                or "gói vay 1" in text
                or "thứ nhất" in text
                or "cưới" in text
                or "lấy vợ" in text
                or "cá nhân" in text
                or "du lịch" in text
            ):
                entity = "loan_type"
                value = "cưới hỏi"
            elif (
                    text == "2"
                    or "nhà" in text
                    or "số 2" in text
                    or "gói 2" in text
                    or "thứ 2" in text
                    or "gói vay 2" in text
            ):
                entity = "loan_type"
                value = "mua nhà"
            elif (
                    text == "3"
                    or "xe" in text
                    or "ô tô" in text
                    or "số 3" in text
                    or "gói 3" in text
                    or "thứ ba" in text
                    or "gói vay 3" in text
            ):
                entity = "loan_type"
                value = "mua xe"

            if entity is None:
                time_sequen = session.get("time_sequen", "not set")
                if time_sequen == 1:
                    session["time_sequen"] = 0
                    session["intent"] = None
                    # intent = session.get('intent', 'not set')
                    response_text = response_config.loan_responses['loan_rej']
                else:
                    session["time_sequen"] = 1
                    response_text = response_config.loan_responses['loan']

            else:
                session["time_sequen"] = 0
                if value == "cưới hỏi":
                    response_text = response_config.loan_responses['loan_1']
                if value == "mua nhà":
                    response_text = response_config.loan_responses['loan_2']
                if value == "mua xe":
                    response_text = response_config.loan_responses['loan_3']

        # Show Balance
        elif intent == "show_balance":
            card_ids = re.findall(
                r"\s\d{11}\s|\s\d{11}$|^\d{11}\s|^\d{11}$",
                text
            )

            if len(card_ids) > 0:
                card_id = card_ids[0].strip()
                session["card_id"] = card_id

            card_id = session.get("card_id", "not set")

            if card_id is None:
                response_text = (
                    "Quý khách vui lòng cung cấp số thẻ "
                    "(số thẻ được in ở mặt sau của thẻ, bao gồm 11 chữ số): "
                )
            else:
                response_text = (
                    "Tài khoản {0} của quý khách đang có số dư là "
                    "11.000.000 vnđ.".format(
                        card_id
                    )
                )
                session["intent"] = None
                session["time_sequen"] = 0

        # Show summary
        elif intent == "summary":
            card_ids = re.findall(
                            r"\s\d{11}\s|\s\d{11}$|^\d{11}\s|^\d{11}$",
                            text
                        )

            if len(card_ids) > 0:
                card_id = card_ids[0].strip()
                session["card_id"] = card_id

            card_id = session.get("card_id", "not set")

            if card_id is None:
                response_text = (
                    "Quý khách vui lòng cung cấp số thẻ "
                    "(số thẻ được in ở mặt sau của thẻ, bao gồm 11 chữ số): "
                )
            else:
                response_text = "Số tài khoản: {0}\n"\
                                "Tên chủ tài khoản: Phạm Hữu Quang \n"\
                                "Chi nhánh: Sun* chi nhánh Hải Dương\n"\
                                "Loại tài khoản: tài khoản bạch kim\n"\
                                "Số dư hiện tại: 11.000.000.000 vnđ.\n"\
                                "Giao dịch gần nhất: 500.000.000 vnđ".format(
                                    card_id
                                )
                session["intent"] = None
                session["time_sequen"] = 0

        # credit_card_limit
        elif intent == "credit_card_limit":
            card_ids = re.findall(
                            r"\s\d{11}\s|\s\d{11}$|^\d{11}\s|^\d{11}$",
                            text
                        )

            if len(card_ids) > 0:
                card_id = card_ids[0].strip()
                session["card_id"] = card_id

            card_id = session.get("card_id", "not set")

            if card_id is None:
                response_text = (
                    "Quý khách vui lòng cung cấp số thẻ "
                    "(số thẻ được in ở mặt sau của thẻ, bao gồm 11 chữ số): "
                )
            else:
                month = datetime.datetime.now().month + 1
                year = datetime.datetime.now().year
                response_text = (
                    "Hạn mức tín dụng của thẻ {0} còn lại là "
                    "40.000.000 vnđ, hạn mức tín dụng tối đa 45.000.000 vnđ. "
                    "Vui lòng thanh toán trước ngày 5/{1}/{2}.".format(
                        card_id, str(month), str(year)
                    )
                )
                session["intent"] = None
                session["time_sequen"] = 0

        elif intent == "bank_infor":
            response_text = get_random_response("bank_infor")
            session["intent"] = None
            session["time_sequen"] = 0

        elif intent == "bank_bot":
            response_text = get_random_response("bank_intro")
            session["intent"] = None
            session["time_sequen"] = 0

        else:
            response_text = get_random_response(intent)

        with open("log.txt", "a") as f_w:
            f_w.write("User: " + text + "\nBot: " + response_text + "\n\n")

        return jsonify({"status": "success", "response": response_text})
    except Exception as e:
        print(e)
        return jsonify(
            {"status": "error", "response": get_random_response("confused")}
        )


if __name__ == "__main__":
    app.run()
