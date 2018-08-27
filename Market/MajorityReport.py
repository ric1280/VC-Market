'''
Created on 11/07/2018

@author: ricar
'''
def majorityReport(checked_job_machines):
    
    quorum = len(checked_job_machines)
    
    #compare variables
    result_machines = []
    for machine in checked_job_machines:
        if machine["status"] != "Error":
            if not result_machines:
                result_machines.append(machine)
            else:
                matched = False
                for i in range(0, len(result_machines)):
                    ### Validate if all variables have the same value
                    
                    
                    if isinstance(result_machines[i], (list,)):
                        machine2 = result_machines[i][0]
                    else:
                        machine2 = result_machines[i]
                    
                    
                    variables2 = machine2["vars"].keys()
                    variables1 = machine["vars"].keys()
                    variables = list(set(variables1) & set(variables2))
                    machines_have_the_same_result = True
                    for var in variables:
                        if str(machine["vars"][var]) != str(machine2["vars"][var]):
                            machines_have_the_same_result = False
                            break
                        
                    if machines_have_the_same_result:
                        
                        
                        if isinstance(result_machines[i], (list,)):
                            result_machines[i].append(machine)
                        else:
                            group = []
                            group.append(machine)
                            group.append(machine2)
                            result_machines[i] = group
                            
                        matched = True
                        #Skip the comparison with the next machines    
                        break
                        #They are not equal then try to compare with the next machine
                    
                if not matched:
                    result_machines.append(machine)
                    
                    
    solution= []
    for i in range(0, len(result_machines)):
    
        if isinstance(result_machines[i], (list,)) and len(result_machines[i]) > quorum/2:
            solution = result_machines[i]
            
            
            break
        
    
    if not solution:
        ### the majority report is based only on quiz and variable list test
        ### because checked_job_machines has a field status with the evaluation of those criterias we shall just return it
        return checked_job_machines
    
    else:
        for i in range(0, len(checked_job_machines)):
            machine_is_in_solution = False
            for j in range(0, len(solution)):
                if checked_job_machines[i]["mid"] == solution[j]["mid"]:
                    checked_job_machines[i]["status"] = "Success"
                    machine_is_in_solution = True
            
            if not machine_is_in_solution:
                checked_job_machines[i]["status"]= "Wrong"
                
        return checked_job_machines
            
                
                            
                
                        
                
                    
                    
                           
    
                        
                    
                    
                
                
                
    
    