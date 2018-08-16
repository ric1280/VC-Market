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
                    variables = variables1 & variables2
                    machines_have_the_same_result = True
                    for var in variables:
                        if machine["vars"][var] != machine2["vars"][var]:
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
                    
                    
    
                        
                    
                    
                
                
                
    
    