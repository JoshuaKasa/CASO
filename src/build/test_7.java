
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;

        public class test_7 {
        
        public static int fibonacci(
        int n) {

        int a = 0;
        
        int b = 1;
        
        n = n - 1;
        
        for (int i = 1; i <= n; i++) {
        
        int s = a + b;
        
        a = b;
        
        b = s;
        
        }
        
        return a;
        
        }
        
        public static int power(
        int base, int exponent) {

        int result = 1;
        
        for (int x = 1; x <= exponent; x++) {
        
        result = result * base;
        
        }
        
        return result;
        
        }
        
            public static void main(String[] args) {

        
            fibonacci(
        7);
            }
        }
        