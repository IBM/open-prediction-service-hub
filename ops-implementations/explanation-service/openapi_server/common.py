
def is_flat_explanation(model_id):
    return model_id == "1"


def get_explanation_name(feature):
    return f'{feature}_explanation'


used_names = ['creditScore', 'income', 'loanAmount', 'monthDuration', 'rate', 'yearlyReimbursement', 'paymentDefault']


def get_feature_names():
    return used_names[:-1]


def get_label_name():
    return used_names[-1]
