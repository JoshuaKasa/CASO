package libraries;
        public class Me {
        
            public String name;
            
            public String surname;
            
        public Me (
        String name, String surname) {

            this.name = name;
            
            this.surname = surname;
            
        }
        
        public  void print_informations(
        ) {

            print_line(
        "Name: " + name);
            print_line(
        "Surname: " + surname);
        }
        
            public String get_name() {
                return this.name;
            }

            public void set_name(String name) {
                this.name = name;
            }
        
            public String get_surname() {
                return this.surname;
            }

            public void set_surname(String surname) {
                this.surname = surname;
            }
        
        @Override
        public String toString() {
            return "Me(" +
        
            "name=" + this.name +
            
            "surname=" + this.surname +
            
            ")";
        }}
        