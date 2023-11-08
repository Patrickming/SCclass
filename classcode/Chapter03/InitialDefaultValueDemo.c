#include <stdio.h> 

int global_var; 

int main()
{
    int local_var;
    local_var = local_var + 3;

    printf("global_var = %d\n", global_var);
    printf("local_var = %d\n", local_var);
    
    return 0;
}
