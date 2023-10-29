def find_dislikes(friends: dict)->set[tuple]:
    """Given a dictionary-based adjacency list of String-based nodes,
       returns a set of all edges in the graph (ie. dislikes who can't be invited together).
       
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A set of edges in the graph represented as tuples
            - An edge should only appear once in the set.
            - Each edge should list node connections in alphabetical order.

       Example
       -------
       >>>friends={
           'Alice':['Bob'],
           'Bob':['Alice', 'Eve'],
           'Eve':['Bob']
       }
       >>>find_dislikes(friends)
       {('Alice','Bob'),('Bob','Eve')}

    """
    dislikes = set()
    for person in friends:
        for dislike in friends[person]:
            if (dislike, person) not in dislikes:
                dislikes.add((person, dislike))
    return dislikes

def generate_all_subsets(friends: dict)->list[list[str]]:
    '''Converts each number from 0 to 2^n - 1 into binary and uses the binary representation
       to determine the combination of guests and returns all possible combinations
      
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list of all possible subsets of friends to invite, represented as lists of strings
       
       Example
       -------
       >>>friends={
           'Alice':['Bob'],
           'Bob':['Alice', 'Eve'],
           'Eve':['Bob']
       }
       >>>generate_all_subsets(friends)
       [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve'], ['Alice', 'Bob'], ['Alice', 'Bob', 'Eve']]
    '''
    friend_list = list(friends.keys())
    n = len(friends)
    
    all_subsets = []

    for i in range(2**n):
        num = i  #convert each number in the range to a binary string
        new_subset = []
        for j in range(n): # to_binary_division approach
            if (num % 2 == 1): # 1 indicates the guest is included
                new_subset = [friend_list[n-1-j]] + new_subset 
            num = num // 2
        all_subsets.append(new_subset)

    return all_subsets


def filter_bad_invites(all_subsets:list, friends:dict)->list[list[str]]:
    '''Removes subsets from all_subsets that contain any pair of friends who
       are in a dislike relationship

       Args:
           all_subsets: a list of all possible friend combinations, each reresented as a list of strings
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list containing only friend combinations that exclude dislike pairs
      
       Example
       -------
       >>>all_subsets = [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve'], ['Alice', 'Bob'], ['Alice', 'Bob', 'Eve']]
       >>>friends={
           'Alice':['Bob'],
           'Bob':['Alice'],
           'Eve':[]
       }  
       >>>filter_bad_invites(all_subsets, friends)
       [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve']]
    '''
    good_invites = all_subsets
    bad_invites = []

    for set in all_subsets:
        for pair in find_dislikes(friends):
            if pair[0] in set and pair[1] in set:
                bad_invites += [set]
    
    for set in bad_invites:
        if set in good_invites:
            good_invites.remove(set)

    return good_invites

def filter_no_dislikes(friends:dict)->tuple[list, dict]:
    '''An optimization that removes friends who are not in any dislikes relationships,
       prior to generating combinations and add them to the invite list.

       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A tuple containing:
            - list of friends not in dislike relations AND 
           - resulting dictionary with these friends removed

       Example
       -------
       >>>friends={
           'Alice':['Bob'],
           'Bob':['Alice', 'Eve'],
           'Cleo':[],
           'Don':[],
           'Eve':['Bob']
       }
       >>>filter_no_dislikes(friends)
       (['Cleo', 'Don'], {'Alice': ['Bob'], 'Bob': ['Alice', 'Eve'], 'Eve': ['Bob']})
    '''
    no_dislikes = []
    new_friends = {}

    for item in friends:
        if friends[item] == []:
            no_dislikes += [item]
        else:
            new_friends[item] = friends[item]

    return no_dislikes, new_friends

def invite_to_dinner(friends: dict)-> list[str]:
    '''Finds the invite combo with the maximum number of guests
       
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list of friends to invite to dinner which maximizes the number of friends on the list
       
       Example
       -------
       >>>friends={
           'Alice':['Bob'],
           'Bob':['Alice', 'Eve'],
           'Cleo':[],
           'Don':[],
           'Eve':['Bob']
       }
       >>>invite_to_dinner(friends)
       ['Alice', 'Eve', 'Cleo', 'Don']
    '''
    all_subsets = generate_all_subsets(friends)
    good_subsets = filter_bad_invites(all_subsets, friends)

    #find the subset which maximizes number of invites
    invite_list = []
    for potential_subset in good_subsets:
        if len(potential_subset) > len(invite_list):
            invite_list = potential_subset

    return invite_list

def invite_to_dinner_optimized(friends:dict)->list:
    '''Finds the combination with the maximum number of guests without computing all combinations

       Functions the same as invite_to_dinner without computing all subsets
       i.e. take out the "good" guests with no dislikes first, and then only generate subsets
       of the "bad" guests. Add in the "good" guests at the end.

       Hint: Call your filter_no_dislikes() function!
       
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list of friends to invite to dinner which maximizes the number of friends on the list
       
       Example
       -------
       >>>friends={
           'Alice':['Bob'],
           'Bob':['Alice', 'Eve'],
           'Cleo':[],
           'Don':[],
           'Eve':['Bob']
       }
       >>>invite_to_dinner(friends)
       ['Alice', 'Eve', 'Cleo', 'Don']
    '''
    better = filter_no_dislikes(friends)
    bad_subsets = generate_all_subsets(better[1])
    good_subsets = filter_bad_invites(bad_subsets, friends)

    #find the subset which maximizes number of invites
    invite_list = []
    for potential_subset in good_subsets:
        if len(potential_subset) > len(invite_list):
            invite_list = potential_subset
    
    invite_list += better[0]

    return invite_list

if __name__ == "__main__":
    friends = {
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Cleo':[],
        'Don':[],
        'Eve':['Bob']
    }
    print(invite_to_dinner(friends))
    print(invite_to_dinner_optimized(friends))

    friends_2 = {
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Eve':['Bob']
    }
    print(invite_to_dinner(friends_2))
    print(invite_to_dinner_optimized(friends_2))

    friends_3 = {
        'Asa':[], 
        'Bear':['Cate'],
        'Cate':['Bear', 'Dave'],
        'Dave':['Cate','Eve'], 
        'Eve':['Dave'], 
        'Finn':['Ginny', 'Ivan'], 
        'Ginny':['Finn', 'Haruki'], 
        'Haruki':['Ginny'], 
        'Ivan':['Finn']
    }
    print(invite_to_dinner(friends_3))
    print(invite_to_dinner_optimized(friends_3))