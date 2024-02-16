
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;

        public class test_12 {
        
        public static int adjustedSum(
        int n) {

        int sum = 0;
        
        for (int i = 1; i <= n; i++) {
        
            if (sum % 2) {
            
        sum = sum + i;
        
                if (i == 5) {
                
        sum = sum + 10;
        
                }
                
                else if (i > 8) {
                
        sum = sum + 5;
        
                }
                
                else {
                
            }
            
            }
            
        }
        
        if (sum > 50) {
        
        sum = sum + 10;
        
        }
        
        else if (sum < 20) {
        
        sum = sum - 5;
        
        }
        
        else {
        
        sum = sum + 1;
        
        }
        
        return sum;
        
        }
        
            public static void main(String[] args) {

        
            adjustedSum(
        10);
            }
        }
        