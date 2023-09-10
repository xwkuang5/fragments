"""The data structure for the factor is referenced from Prof. Daphne Koller's coursera course "Probabilistic Graphical Models"
"""

import numpy as np


def ismember(a, b):
    bind = {}
    for index, value in enumerate(b):
        if value not in bind:
            bind[value] = index
    return [bind.get(value, None) for value in a]


"""
TODO: 
    1. vectorization
    2. handle multiple variables at once in restrict, multiply and sumout
"""


class Factor:
    def __init__(self, var, card, val):
        """Represent factor using a multi-dimensional array
        
        Arguments:
        var     -- a np array of variable names, i.e., scope of the factor
        card    -- a np array of cardinality values corresponding to var, i.e., scopre of the variables
        val     -- a np array of values for every possible assignment to the variables. If var = X_1, X_2, X_3 and card = 2, 2, 2, then val should be given in order of (1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 2, 2), (2, 1, 1) and so on
        """
        if len(var) != len(card) or np.prod(card) != len(val):
            raise Exception("invalid initialization for Factor initialization")
        self._var = np.copy(var)
        self._card = np.copy(card)
        self._val = np.copy(val)

    def factor_copy(factor):
        return Factor(factor.var, factor.card, factor.val)

    @property
    def var(self):
        return self._var

    @property
    def card(self):
        return self._card

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        # check validity
        self._val = value

    # @val.setter
    # def val(self, index, value):
    #     # check validity
    #     self._val[index] = value

    def assignment_to_index(assignment, cardinality):
        """Returns the index of the given assignment in a factor with card = cardinality

        Arguments:
        assignment  -- a np array of values of the variables, e.g., X_1 = 1, X_2 = 2, X_3 = 3 => [1, 2, 3]
        cardinality -- a np array of cardinality values corresponding to var

        Returns:
        index       -- index of the given assignment in a factor with card = cardinality; note index starts from 0
        """
        if any([assignment[i] < 1 for i in range(len(assignment))]):
            raise Exception("invalid assignment value: %s" % str(assignment))
        if len(assignment) != len(cardinality) or any(
            [assignment[i] > cardinality[i] for i in range(len(assignment))]):
            raise Exception("assignment[%s] and cardinality[%s] do not match" %
                            (str(assignment), str(cardinality)))

        index = 0
        for i in range(len(assignment)):
            # int64 + uint64 -> float64 wtf! well documented strange thing here https://github.com/numpy/numpy/issues/5745
            index = index + (assignment[i] - 1) * np.prod(cardinality[i + 1:])
        return int(index)

    def index_to_assignment(index, cardinality):
        """Returns the assignment of the given index in a factor with card = cardinality

        Arguments:
        index       -- the index to be queried; note index starts from 0
        cardinality -- a np array of cardinality values corresponding to var

        Returns:
        assignment  -- a np array corresponding to assignment of the given index in a factor with card = cardinality
        """
        if index < 0 or index >= np.prod(cardinality):
            raise Exception("index[%d] out of range for cardinality[%s]" %
                            (index, str(cardinality)))
        assignment = np.zeros(len(cardinality), dtype=np.uint8)
        for i in range(len(cardinality)):
            assignment[i] = index / np.prod(cardinality[i + 1:]) + 1
            index = index % np.prod(cardinality[i + 1:])

        return assignment

    def get_value_of_assignment(factor, assignment):
        """Returns the value of the assignment in the factor

        Arguments:
        factor      -- the factor to be queried
        assignment  -- a np array corresponding to the assignment to be queried

        Returns:
        val         -- value of the assignment in the factor
        """
        if len(assignment) != len(factor.var):
            raise Exception(
                "length of assignment[%d] does not match the number of variables in the factor"
                % len(assignment))
        index = Factor.assignment_to_index(assignment, factor.card)

        return factor.val[index]

    def set_value_of_assignment(factor, assignment, val):
        """Returns a new factor with the value for assignment set to val

        Arguments:
        factor      -- the factor to be queried
        assignment  -- a np array corresponding to the assignment to be queried
        val         -- the value to be set

        Returns:
        ret_factor  -- a new factor with the value for assignment set to val
        """
        if len(assignment) != len(factor.var):
            raise Exception(
                "length of assignment[%d] does not match the number of variables in the factor"
                % len(assignment))

        ret_factor = Factor.factor_copy(factor)
        index = Factor.assignment_to_index(assignment, ret_factor.card)
        ret_factor.val[index] = val

        return ret_factor

    def restrict(factor, variable, value):
        """Restrict the variable in the factor to the value provided

        Arguments:
        factor      -- the factor to be restricted
        variable    -- the variable to be restricted
        value       -- the value to set to

        Returns
        new_factor  -- the new factor after setting the value
        """
        if variable not in factor.var:
            raise Exception("variable[%d] is not in factor" % variable)
        index = np.where(factor.var == variable)[0][0]

        new_factor = Factor.factor_copy(factor)

        for i in range(np.prod(new_factor.card)):
            assignment = Factor.index_to_assignment(i, new_factor.card)
            if assignment[index] != value:
                new_factor.val[i] = 0

        return new_factor

    def multiply(factor_A, factor_B):
        """Return a new factor which is the product of the two given factors

        Arguments:
        factor_A    -- factor
        factor_B    -- factor

        Returns:
        new_factor  -- a new factor which is the product of factor_A and factor_B
        """

        # Find intersection between scopes of the two factors
        common_var = np.intersect1d(factor_A.var, factor_B.var)
        # Find index of the common variables in factor A
        common_var_index_in_A = ismember(common_var, factor_A.var)
        # Find index of the common variables in factor B
        common_var_index_in_B = ismember(common_var, factor_B.var)
        # Check if cardinality of common variables match in the two factors
        for i in range(len(common_var)):
            if factor_A.card[common_var_index_in_A[i]] != factor_B.card[common_var_index_in_B[i]]:
                raise Exception(
                    "cardinality of variables in factor A and factor B do not match"
                )

        # Find the scope of the resulting factor
        all_var = np.union1d(factor_A.var, factor_B.var)

        # Initialize the cardinality of the resulting factor
        all_card = np.zeros((len(all_var)), dtype=np.uint8)
        # Find index of the variable of factor A in the resulting factor
        var_A_index_in_all_var = ismember(factor_A.var, all_var)
        # Find index of the variable of factor B in the resulting factor
        var_B_index_in_all_var = ismember(factor_B.var, all_var)
        # Set the cardinality of the resulting factor
        all_card[var_A_index_in_all_var] = factor_A.card
        all_card[var_B_index_in_all_var] = factor_B.card

        # Initialize the values of the new factor
        all_val = np.zeros((np.prod(all_card)))
        for i in range(np.prod(all_card)):
            # Generate one assignment of the new factor
            all_assignment = Factor.index_to_assignment(i, all_card)
            # Find the assignment in factor A that corresponds to the current assignment in the new factor
            assignment_A = all_assignment[var_A_index_in_all_var]
            # Find the assignment in factor B that corresponds to the current assignment in the new factor
            assignment_B = all_assignment[var_B_index_in_all_var]
            # Get assignment value from factor A
            val_A = Factor.get_value_of_assignment(factor_A, assignment_A)
            # Get assignment value from factor B
            val_B = Factor.get_value_of_assignment(factor_B, assignment_B)
            # Multiply the two assignment values to get value for the assignment in the new factor
            all_val[i] = val_A * val_B

        # Construct the new factor and return
        new_factor = Factor(all_var, all_card, all_val)
        return new_factor

    def sumout(factor, variable):
        """Sum out the given variable from the factor

        Arguments:
        factor      -- the factor to be marginalized
        variable    -- the variable to be summed out

        Returns:
        new_factor  -- the given factor with the variable summed out
        """

        # check whether variable is in factor
        if variable not in factor.var:
            raise Exception("variable[%d] is not in factor[%s]" % (variable,
                                                                   factor.var))

        # Find the scope of the resulting factor
        new_var = np.setdiff1d(factor.var, variable)
        # Find index of variable of new factor in old factor
        new_var_index_in_factor = ismember(new_var, factor.var)
        # Find cardinality of new factor from old factor
        new_card = np.copy(factor.card[new_var_index_in_factor])
        # Initialize values for new factor
        new_val = np.zeros(np.prod(new_card))

        for i in range(np.prod(factor.card)):
            # Find assignment of old factor
            assignment_in_factor = Factor.index_to_assignment(i, factor.card)
            # Find assignment of old factor in new factor
            assignment_in_new_factor = assignment_in_factor[
                new_var_index_in_factor]
            # Find index of assingment in new factor
            index_in_new_factor = Factor.assignment_to_index(
                assignment_in_new_factor, new_card)
            # Add values in old factor to new factor
            new_val[index_in_new_factor] += Factor.get_value_of_assignment(
                factor, assignment_in_factor)

        return Factor(new_var, new_card, new_val)

    def normalize(factor):
        """Normalize a factor

        Arguments:
        factor  -- the factor to be normalized

        Returns:
        new_factor  -- the normalized factor
        """

        new_factor = Factor.factor_copy(factor)
        new_factor.val = new_factor.val / np.sum(new_factor.val)

        return new_factor

    def inference(factorList,
                  queryVariables,
                  orderedListOfHiddenVariables,
                  evidenceList,
                  verbose=True):
        """Perform inference on the bayes net

        Arguments:
        factorList                      -- a list of factor defining the bayes net
        queryVariables                  -- a list of variables to query
        orderedListOfHiddenVariables    -- a variables elimination order
        evidenceList                    -- a dictionary of {variable: value}
        verbose                         -- verbose mode

        Returns:
        new_factor                      -- the factor representing the inference result
        """

        # observe evidence
        for idx in range(len(factorList)):
            for key, value in evidenceList.items():
                # If evidence in factor scope, restrict
                if key in factorList[idx].var:
                    factorList[idx] = Factor.restrict(factorList[idx], key,
                                                      value)

        # store intermediate factor
        tmp_factor = None
        for variable in orderedListOfHiddenVariables:
            # keep track of which factor has been multipled
            remove_list_idx = []
            for idx in range(len(factorList)):
                if variable in factorList[idx].var:
                    # First factor containing the variable to be eliminated => initialize intermediate
                    if tmp_factor == None:
                        tmp_factor = factorList[idx]
                    else:
                        tmp_factor = Factor.multiply(tmp_factor,
                                                     factorList[idx])
                    # factList[idx] was multiplied => add to removal list
                    remove_list_idx.append(idx)
            # remove factor which has been multiplied

            for idx in reversed(range(len(remove_list_idx))):
                del factorList[remove_list_idx[idx]]
            # All factors containing the variable to be eliminated have been multiplied => sum out the variable
            tmp_factor = Factor.sumout(tmp_factor, variable)

            # Print-out
            tmp_factor_name = []
            for var in tmp_factor.var:
                for key, value in factor_name.items():
                    if value == var:
                        tmp_factor_name.append(key)
            if verbose:
                print("IntermediateFactor(%s): %s" % (tmp_factor_name,
                                                      tmp_factor.val))

            # Add resulting factor back to factorList
            factorList.append(tmp_factor)
            # Set intermediate factor to be None for next iteration
            tmp_factor = None

        ret_factor = None
        # multiply all the remaining factors in the factorList
        for idx in range(len(factorList)):
            if ret_factor == None:
                ret_factor = factorList[idx]
            else:
                ret_factor = Factor.multiply(ret_factor, factorList[idx])
            # Print-out
            tmp_factor_name = []
            for var in ret_factor.var:
                for key, value in factor_name.items():
                    if value == var:
                        tmp_factor_name.append(key)
            if verbose:
                print("IntermediateFactor(%s): %s" % (tmp_factor_name,
                                                      ret_factor.val))

        # normalize the final factor
        ret_factor = Factor.normalize(ret_factor)

        return ret_factor

if __name__ == "__main__":
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
