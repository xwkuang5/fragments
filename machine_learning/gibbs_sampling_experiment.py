import numpy as np
from bayesnet import Factor

factor_name = {"FS": 1, "FM": 2, "NA": 3, "FB": 4, "NDG": 5, "FH": 6}
variable_val = {"YES": 1, "NO": 2}

# Fido is sick factor
var_FS = np.array([factor_name["FS"]])
card_FS = np.array([2])
val_FS = np.array([0.05, 0.95])
factor_FS = Factor(var_FS, card_FS, val_FS)

# Full moon factor
var_FM = np.array([factor_name["FM"]])
card_FM = np.array([2])
val_FM = np.array([1. / 28, 27. / 28])
factor_FM = Factor(var_FM, card_FM, val_FM)

# Neighbor away factor
var_NA = np.array([factor_name["NA"]])
card_NA = np.array([2])
val_NA = np.array([0.3, 0.7])
factor_NA = Factor(var_NA, card_NA, val_NA)

# Factor of Fido is sick and food in Fido's bowl
var_FS_FB = np.array([factor_name["FS"], factor_name["FB"]])
card_FS_FB = np.array([2, 2])
val_FS_FB = np.array([0.6, 0.4, 0.1, 0.9])
factor_FS_FB = Factor(var_FS_FB, card_FS_FB, val_FS_FB)

# Factor of full moon, neighbor away and neighbor's dog is howling
var_FM_NA_NDG = np.array(
    [factor_name["FM"], factor_name["NA"], factor_name["NDG"]])
card_FM_NA_NDG = np.array([2, 2, 2])
val_FM_NA_NDG = np.array([0.8, 0.2, 0.4, 0.6, 0.5, 0.5, 0, 1])
factor_FM_NA_NDG = Factor(var_FM_NA_NDG, card_FM_NA_NDG, val_FM_NA_NDG)

# Factor of full moon, neighbor's dog is howling, Fido is sick and Fido howls
var_FM_NDG_FS_FH = np.array([
    factor_name["FM"], factor_name["NDG"], factor_name["FS"], factor_name["FH"]
])
card_FM_NDG_FS_FH = np.array([2, 2, 2, 2])
val_FM_NDG_FS_FH = np.array([
    0.99, 0.01, 0.65, 0.35, 0.9, 0.1, 0.4, 0.6, 0.75, 0.25, 0.2, 0.8, 0.5, 0.5,
    0, 1
])
factor_FM_NDG_FS_FH = Factor(var_FM_NDG_FS_FH, card_FM_NDG_FS_FH,
                             val_FM_NDG_FS_FH)

factor_list = [
    factor_FS, factor_FM, factor_NA, factor_FS_FB, factor_FM_NA_NDG,
    factor_FM_NDG_FS_FH
]

# part b
query_variables = [factor_name["FH"]]
ordered_list_of_hidden_variables = [
    factor_name["NA"], factor_name["FS"], factor_name["FB"], factor_name["FM"],
    factor_name["NDG"]
]
evidence_list = {}
prior_FH_howl = Factor.inference(factor_list.copy(), query_variables,
                                 ordered_list_of_hidden_variables,
                                 evidence_list)
print("[part b] prior probability of Fido howling is %f, not howling is %f" %
      (prior_FH_howl.val[0], prior_FH_howl.val[1]))

# part c
evidence_list = {
    factor_name["FH"]: variable_val["YES"],
    factor_name["FM"]: variable_val["YES"]
}
query_variables = [factor_name["FS"]]
ordered_list_of_hidden_variables = [
    factor_name["FH"], factor_name["FM"], factor_name["NA"],
    factor_name["NDG"], factor_name["FB"]
]
posterior_FIDO_sick = Factor.inference(factor_list.copy(), query_variables,
                                       ordered_list_of_hidden_variables,
                                       evidence_list)
print("[part c] posterior probability of Fido is sick is %f, not sick is %f" %
      (posterior_FIDO_sick.val[0], posterior_FIDO_sick.val[1]))

# part d
evidence_list = {
    factor_name["FH"]: variable_val["YES"],
    factor_name["FM"]: variable_val["YES"],
    factor_name["FB"]: variable_val["YES"]
}
query_variables = [factor_name["FS"]]
ordered_list_of_hidden_variables = [
    factor_name["FH"], factor_name["FM"], factor_name["FB"], factor_name["NA"],
    factor_name["NDG"]
]
posterior_FIDO_sick = Factor.inference(factor_list.copy(), query_variables,
                                       ordered_list_of_hidden_variables,
                                       evidence_list)
print("[part d] posterior probability of Fido is sick is %f, not sick is %f" %
      (posterior_FIDO_sick.val[0], posterior_FIDO_sick.val[1]))
