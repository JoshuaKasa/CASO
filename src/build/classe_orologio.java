
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;
        
        public class classe_orologio {
        
            public static void main(String[] args) {

        
public class Orologio {

            public int ore;
            
            public int minuti;
            
            public int secondi;
            
            public String data;
            
        public Orologio (
        int ore, int minuti, int secondi, String data) {

            this.ore = ore;
            
            this.minuti = minuti;
            
            this.secondi = secondi;
            
            this.data = data;
            
        }
        
        public static void impostaOrario(
        int ore_, int minuti_, int secondi_) {

        ore = ore_;
        
        minuti = minuti_;
        
        secondi = secondi_;
        
        }
        
        public static String visualizzaOrario(
        ) {

        return "Sono le " + ore + ":" + minuti + ":" + secondi;
        
        }
        
        public static void incrementaOrario(
        ) {

        secondi = secondi + 1;
        
        }
        
        public static String visualizzaData(
        ) {

        return "Oggi e' il: " + data;
        
        }
        
            public int get_ore() {
                return this.ore;
            }

            public void set_ore(int ore) {
                this.ore = ore;
            }
        
            public int get_minuti() {
                return this.minuti;
            }

            public void set_minuti(int minuti) {
                this.minuti = minuti;
            }
        
            public int get_secondi() {
                return this.secondi;
            }

            public void set_secondi(int secondi) {
                this.secondi = secondi;
            }
        
            public String get_data() {
                return this.data;
            }

            public void set_data(String data) {
                this.data = data;
            }
        
        @Override
        public String toString() {
            return "Orologio(" +
        
            "ore=" + this.ore +
            
            "minuti=" + this.minuti +
            
            "secondi=" + this.secondi +
            
            "data=" + this.data +
            
            ")";
        }}
        
            }
        }
        
