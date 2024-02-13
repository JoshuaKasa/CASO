
        // This is the general header template for the transpiled code
        import java.util.Scanner;
        import java.util.ArrayList;

        public class test_10 {
        
            public static void main(String[] args) {

        
public class Person {

            public string name;
            
            public string surname;
            
            public string gender;
            
            public string age;
            
        public Person (
        string name, string surname, string gender, string age) {

            this.name = name;
            
            this.surname = surname;
            
            this.gender = gender;
            
            this.age = age;
            
        }
        
            public string get_name() {
                return this.name;
            }

            public void set_name(string name) {
                this.name = name;
            }
        
            public string get_surname() {
                return this.surname;
            }

            public void set_surname(string surname) {
                this.surname = surname;
            }
        
            public string get_gender() {
                return this.gender;
            }

            public void set_gender(string gender) {
                this.gender = gender;
            }
        
            public string get_age() {
                return this.age;
            }

            public void set_age(string age) {
                this.age = age;
            }
        
        @Override
        public String toString() {
            return "Person(" +
        
            "name=" + this.name +
            
            "surname=" + this.surname +
            
            "gender=" + this.gender +
            
            "age=" + this.age +
            
            ")";
        }}
        
public class Student extends Person {

            public bool promosso;
            
        public Student (
        bool promosso) {

            this.promosso = promosso;
            
        }
        
            public bool get_promosso() {
                return this.promosso;
            }

            public void set_promosso(bool promosso) {
                this.promosso = promosso;
            }
        
        @Override
        public String toString() {
            return "Student(" +
        
            "promosso=" + this.promosso +
            
            ")";
        }}
        
            }
        }
        