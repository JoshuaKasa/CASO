package libraries;
        public class standard {
        
            public int STD_SUCCESS;
            
            public int STD_FAILURE;
            
        public standard (
        int STD_SUCCESS, int STD_FAILURE) {

            this.STD_SUCCESS = STD_SUCCESS;
            
            this.STD_FAILURE = STD_FAILURE;
            
        }
        
        public  void Halt(
        ) {

        System.exit(STD_FAILURE);
        
        }
        
        public  void Pass(
        ) {

        System.exit(STD_SUCCESS);
        
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
        
            public int get_STD_SUCCESS() {
                return this.STD_SUCCESS;
            }

            public void set_STD_SUCCESS(int STD_SUCCESS) {
                this.STD_SUCCESS = STD_SUCCESS;
            }
        
            public int get_STD_FAILURE() {
                return this.STD_FAILURE;
            }

            public void set_STD_FAILURE(int STD_FAILURE) {
                this.STD_FAILURE = STD_FAILURE;
            }
        
        @Override
        public String toString() {
            return "standard(" +
        
            "STD_SUCCESS=" + this.STD_SUCCESS +
            
            "STD_FAILURE=" + this.STD_FAILURE +
            
            ")";
        }}
        