stu_form_reponses: dict = {
    200: {
        "description": "学生验证成功！",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    },

    404: {
        "description": "学生验证失败！",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    },

    403: {
        "description": "拒绝访问",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    },

}
