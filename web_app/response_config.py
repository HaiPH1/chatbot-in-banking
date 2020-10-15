supported_cards = ["thẻ tín dụng", "thẻ credit", "thẻ debit",
                   "thẻ ghi nợ", "thẻ atm"]

affirm_message = [
    "yes", "vâng", "đúng",
    "đúng vậy", "đúng thế",
    "đúng rồi", "ừ", "chính xác",
    "ok", "okie"
]

# dict of response for each type of basic intent
default_responses = {
    "greet": [
        "Kính chào quý khách, quý khách cần trợ giúp gì ạ?",
        "Quý khách cần trợ giúp gì ạ?",
        "Sun* bank xin kính chào quý khách.",
        "Vâng, chào bạn. Tôi có thể giúp gì cho bạn."
    ],
    "goodbye": [
        "Hẹn gặp lại quý khách sau.\nChào quý khách.",
        "Cảm ơn quý khách đã sử dụng dịch vụ của chúng tôi. Tạm biệt.",
        "Cảm ơn quý khách đã sử dụng dịch vụ của chúng tôi. "
        "Tạm biệt quý khách."
    ],
    "affirm": ["vâng", "tôi đã hiểu"],
    "confused": [
        "Xin lỗi, tôi chưa được huấn luyện để trả lời những câu hỏi của bạn.",
        "Xin lỗi anh chị, em chưa được chuẩn bị để trả lời những câu hỏi này."
    ],
    "thanks": [
        "Dạ không có gì ạ. Quý khách còn cần trợ giúp gì nữa không ạ?",
        "Dạ không có gì ạ.",
        "Dạ không có gì ạ. Cảm ơn quý khách đã sử dụng dịch vụ của ngân hàng."
    ],
    "bank_infor": ["Tổng đài chăm sóc khách hàng của Sun* bank là 19001000."],
    "bank_intro": [
        "Em có thể hỗ trợ một số công việc sau: \n"
        " 1. Hỗ trợ thông tin làm thẻ mới.\n"
        " 2. Báo mất thẻ/khóa thẻ/sự cố thẻ. \n"
        " 3. Thông tin chi tiết về tài khoản"
        "/ kiểm tra số dư tài khoản.\n"
        " 4. Kiểm tra thông tin tín dụng/ hạn mức tín dụng \n"
        " 5. Thông tin về các khoản vay/ gói vay \n"
        " 6. Thông tin về phí dịch vụ của ngân hàng."
    ],
}

loan_responses = {
    "loan_rej":
        "Chúng tôi không hỗ trợ mục đích vay này hoặc tin nhắn không liên quan"
        " tới việc hỗ trợ gói vay. Bạn có cần hỗ trợ gì nữa không?",
    "loan":
        "Chúng tôi cung cấp 3 gói vay hiện tại.\n"
        "1.Gói vay cá nhân(cưới hỏi, du lịch, học tập etc)\n"
        "2.Khoản vay mua nhà\n3.Khoản vay mua ô tô\n"
        "Quý khách cần mang theo các giấy tờ cần thiết như chứng minh thư "
        "nhân dân và một số giấy tờ chứng minh thu nhập đến quầy của chúng "
        "tôi để được hỗ trợ.\n Để biết thông tin chi tiết các khoản vay, "
        "chọn 1, 2 hoặc 3 ứng với từng khoản vay.\nXin cảm ơn.",
    "loan_1":
        "Chúng tôi hỗ trợ gói vay lên tới 200 triệu vnđ cho mục đích cưới hỏi,"
        " quý khách cần mang mang theo các giấy tờ sau tới chi nhánh Sun* gần "
        "nhất của chúng tôi để đăng kí.\n"
        "1. Chứng minh thư nhân dân\n"
        "2. Sổ hộ khẩu\n"
        "3. Vợ sắp cưới của bạn --> yêu cầu chữ ký của cả 2 vợ chồng.",
    "loan_2":
        "Chúng tôi hỗ trợ gói vay lên tới 500 triệu vnđ cho mục đích mua nhà,"
        " quý khách cần mang mang theo các giấy tờ sau tới chi nhánh Sun* gần "
        "nhất của chúng tôi để đăng kí.\n"
        "1. Chứng minh thư nhân dân\n"
        "2. Sổ hộ khẩu\n"
        "3. Sao kê lương 3 tháng gần nhất",
    "loan_3":
        "Chúng tôi hỗ trợ gói vay lên tới 200 triệu vnđ cho mục đích mua xe,"
        " quý khách cần mang mang theo các giấy tờ sau tới chi nhánh Sun* gần"
        " nhất của chúng tôi để đăng kí.\n"
        "1. Chứng minh thư nhân dân\n"
        "2. Sổ hộ khẩu\n"
        "3. Sao kê lương 3 tháng gần nhất\n"
        "4. Giấy phép lái xe ứng với loại phương tiện bạn muốn mua"
}

new_card_response = {
    "new_card_reject":
        "Chúng tôi không hỗ trợ loại thẻ này hoặc tin nhắn không liên quan tới"
        " việc hỗ trợ làm thẻ. Quý khách có cần hỗ trợ gì nữa không ạ?",
    "new_card_intro":
        "Chúng tôi có thể có 2 loại thẻ sau. Quý khách cần làm thẻ nào? \n"
        "1. Thẻ tín dụng/Credit card \n"
        "2. Thẻ ghi nợ/thẻ Atm\n"
        "Quý khách có thể chọn 1/2 hoặc cung cấp tên loại thẻ bạn muốn làm.",
    "new_card_info":
        "Để làm {0} quý khách cần mang mang theo các giấy tờ sau tới chi nhánh"
        " Sun* gần nhất của chúng tôi để đăng kí.\n"
        "1. Chứng minh thư nhân dân\n"
        "2. Sổ hộ khẩu\n"
        "3. Sao kê lương 3 tháng gần nhất",
}

card_charge = {
    "card_charge_intro":
        "Phí sử dụng thẻ tín dụng/credit là 300.000 vnđ/năm."
        " Trong năm đầu tiên phát hành thẻ, chúng tôi sẽ hoàn lại 100% phí "
        "thường niên năm đầu tiên.\n"
        "Thẻ ATM được miễn phí phí sử dụng thẻ trong suốt thời gian sử dụng. "
        "Phí SMS banking là 11.000 vnđ/tháng.",
}
