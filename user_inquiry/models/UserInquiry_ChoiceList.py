def FIXED_SUBJECT_CHOICES_LIST():
    FIXED_SUBJECT_CHOICES_LIST = (
            (0, 'スパム'),
            (1, '暴言'),
            (2, '第三者の権利侵害'),
            (3, '悪意ある内容'),
            (4, 'その他不適切な内容を含む'),
            (5, '運営管理者の介入が必要'),
            (90, 'その他'),
        )
    return FIXED_SUBJECT_CHOICES_LIST

def SITUATION_CHOICES_LIST():
    SITUATION_CHOICES_LIST = (
            (0, '未対応'),
            (11, '状況調査中'),
            (12, '事実関係確認中'),
            (13, '照会者への確認中'),
            (14, '関係者への確認中'),
            (80, 'その他対応中'),
            (90, '完了'),
        )
    return SITUATION_CHOICES_LIST