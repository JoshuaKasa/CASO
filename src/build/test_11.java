
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;

        public class test_11 {
        
            public static void main(String[] args) {

        
public class Film {

            public string titolo;
            
            public string regista;
            
            public string genere;
            
            public int durata;
            
        public Film (
        string titolo, string regista, string genere, int durata) {

            this.titolo = titolo;
            
            this.regista = regista;
            
            this.genere = genere;
            
            this.durata = durata;
            
        }
        
        public static bool is_durata_sufficiente(
        ) {

        return durata > 60;
        
        }
        
        public static empty aggiorna_durata(
        int nuova_durata) {

        durata = nuova_durata;
        
        }
        
            public string get_titolo() {
                return this.titolo;
            }

            public void set_titolo(string titolo) {
                this.titolo = titolo;
            }
        
            public string get_regista() {
                return this.regista;
            }

            public void set_regista(string regista) {
                this.regista = regista;
            }
        
            public string get_genere() {
                return this.genere;
            }

            public void set_genere(string genere) {
                this.genere = genere;
            }
        
            public int get_durata() {
                return this.durata;
            }

            public void set_durata(int durata) {
                this.durata = durata;
            }
        
        @Override
        public String toString() {
            return "Film(" +
        
            "titolo=" + this.titolo +
            
            "regista=" + this.regista +
            
            "genere=" + this.genere +
            
            "durata=" + this.durata +
            
            ")";
        }}
        
            }
        }
        
