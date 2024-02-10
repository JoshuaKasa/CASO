
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;

        public class math {
        
        public static int power(
        int base, int exponent) {

        int result = 1;
        
        for (int i = 1; i <= exponent; i++) {
        
        result = result * base;
        
        }
        
        return result;
        
        }
        
        public static float sqrt(
        int x) {

        return (float)Math.sqrt(x);
        
        }
        
        public static float log(
        float x) {

        return (float)Math.log(x);
        
        }
        
        public static float sin(
        float angle) {

        return (float)Math.sin(angle);
        
        }
        
        public static float cos(
        float angle) {

        return (float)Math.cos(angle);
        
        }
        
        public static float tan(
        float angle) {

        return (float)Math.tan(angle);
        
        }
        
            public static void main(String[] args) {

        
            }
        }
        
