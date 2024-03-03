
        public class standard {
        
        public standard (
        ) {

        }
        
        public void print_line(
        String s) {

        System.out.println(s);
        
        }
        
        public String read_line(
        String prompt) {

        System.out.print(prompt);
	return new java.util.Scanner(System.in).nextLine();
        
        }
        
        @Override
        public String toString() {
            return "standard(" +
        
            ")";
        }}
        
