from definitions import *

class Conversion:
    def to_coordinate(n): # Examples: 0 = (1,1) ; 1 = (1,2) ; ... ; 9 = (2,5) ; 21 = (5,2)
        n+=1
        return (n-1)//5 +1, n-((n-1)//5 * 5)

    def to_serial(xy):
        return (xy[0]-1)*5 + xy[1] -1

def mid_point(coordinate1,coordinate2):
    x1,y1,x2,y2=coordinate1[0],coordinate1[1],coordinate2[0],coordinate2[1]
    return [int((x1+x2)/2),int((y1+y2)/2)]

def connections():
    return_dict={}
    for n in range(0,TOTAL_INTERSECTIONS):
        return_dict[n]=[]
        i,j=Conversion.to_coordinate(n)

        if (i+j)%2 == 0: # Even sum: slanted connections too
            for ij in [[i-1,j],[i+1,j],[i,j-1],[i,j+1],[i-1,j-1],[i+1,j+1],[i-1,j+1],[i+1,j-1]]: #upto 8 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS: #filter those out of range
                    return_dict[n].append(Conversion.to_serial([ij[0],ij[1]]))

            
        else: #Odd sum: no slanted connections
            for ij in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]: #upto 4 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS:
                    return_dict[n].append(Conversion.to_serial([ij[0],ij[1]]))
    
    return return_dict

def jump_connections():
    return_dict={}
    for n in range(0,TOTAL_INTERSECTIONS):
        return_dict[n]=[]
        i,j=Conversion.to_coordinate(n)

        if (i+j)%2 == 0: # Even sum: slanted connections too
            for ij in [[i-2,j],[i+2,j],[i,j-2],[i,j+2],[i-2,j-2],[i+2,j+2],[i-2,j+2],[i+2,j-2]]: #upto 8 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS: #filter those out of range
                    return_dict[n].append({
                        'jump_destination': Conversion.to_serial([ij[0],ij[1]]),
                        'jump_over': Conversion.to_serial(mid_point([ij[0],ij[1]],[i,j]))
                        })
            
        else: #Odd sum: no slanted connections
            for ij in [[i-2,j],[i+2,j],[i,j-2],[i,j+2]]: #upto 4 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS:
                    return_dict[n].append({
                        'jump_destination': Conversion.to_serial([ij[0],ij[1]]),
                        'jump_over': Conversion.to_serial(mid_point([ij[0],ij[1]],[i,j]))
                        })

    return return_dict

# Look up values
CONNECTIONS=connections()
JUMP_CONNECTIONS=jump_connections()
