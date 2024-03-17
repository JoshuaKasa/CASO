package libraries;
        public class List {
        
            public int length;
            
            public int[] array_data;
            
        public List (
        int length, int[] array_data) {

            this.length = length;
            
            this.array_data = array_data;
            
        }
        
        public  int increment(
        ) {

            length = length + 1;
            
        return length;
        
        }
        
        public  void push(
        int value) {

            array_data[length] = value;
            
            increment(
        );
        }
        
            public int get_length() {
                return this.length;
            }

            public void set_length(int length) {
                this.length = length;
            }
        
            public int[] get_array_data() {
                return this.array_data;
            }

            public void set_array_data(int[] array_data) {
                this.array_data = array_data;
            }
        
        @Override
        public String toString() {
            return "List(" +
        
            "length=" + this.length +
            
            "array_data=" + this.array_data +
            
            ")";
        }}
        