package libraries;
        public class Type {
        
            public ANY value;
            
        public Type (
        ANY value) {

            this.value = value;
            
        }
        
            public ANY get_value() {
                return this.value;
            }

            public void set_value(ANY value) {
                this.value = value;
            }
        
        @Override
        public String toString() {
            return "Type(" +
        
            "value=" + this.value +
            
            ")";
        }}
        