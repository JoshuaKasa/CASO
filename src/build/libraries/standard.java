package libraries;
        public class standard {
        
        public standard (
        ) {

        }
        
        public static  void print_line(
        String s) {

        System.out.println(s);
        
        }
        
        public static  String read_line(
        String prompt) {

        System.out.print(prompt);
	return new java.util.Scanner(System.in).nextLine();
        
        }
        
        public static  int read_int(
        String prompt) {

        System.out.print(prompt);
	return new java.util.Scanner(System.in).nextInt();
        
        }
        
        @Override
        public String toString() {
            return "standard(" +
        
            ")";
        }}
        
