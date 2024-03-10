package libraries;
        public class Hello {
        
            public int age;
            
        public Hello (
        int age) {

            this.age = age;
            
        }
        
        public  String say_hello(
        ) {

        return "Hello, World! I am " + age + " years old.";
        
        }
        
        public  String try_object(
        ) {

        return "This is a test.";
        
        }
        
            public int get_age() {
                return this.age;
            }

            public void set_age(int age) {
                this.age = age;
            }
        
        @Override
        public String toString() {
            return "Hello(" +
        
            "age=" + this.age +
            
            ")";
        }}
        