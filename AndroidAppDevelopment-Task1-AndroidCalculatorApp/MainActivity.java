package com.example.calculatorapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {


    TextView display;

    StringBuilder expression = new StringBuilder();



    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);



        display = findViewById(R.id.display);



        // Number Buttons

        int[] numberButtons = {

                R.id.btn0,
                R.id.btn1,
                R.id.btn2,
                R.id.btn3,
                R.id.btn4,
                R.id.btn5,
                R.id.btn6,
                R.id.btn7,
                R.id.btn8,
                R.id.btn9

        };



        View.OnClickListener numberClickListener = view -> {

            Button button = (Button) view;

            expression.append(button.getText());

            display.setText(expression.toString());

        };



        for (int id : numberButtons) {

            findViewById(id).setOnClickListener(numberClickListener);

        }




        // Decimal Button

        findViewById(R.id.btnDot).setOnClickListener(view -> {


            String current = expression.toString();


            // If expression is empty or ends with an operator,
            // start the new number as "0." instead of appending
            // a lone dot to nothing / after an operator.
            if (current.isEmpty() ||
                    current.charAt(current.length() - 1) == '+' ||
                    current.charAt(current.length() - 1) == '-' ||
                    current.charAt(current.length() - 1) == '*' ||
                    current.charAt(current.length() - 1) == '/') {

                expression.append("0.");

                display.setText(expression.toString());

                return;
            }


            String[] parts = current.split("[+\\-*/]");


            if (parts.length > 0 && !parts[parts.length - 1].contains(".")) {


                expression.append(".");


                display.setText(expression.toString());

            }


        });





        // Operators

        findViewById(R.id.btnPlus)
                .setOnClickListener(view -> addOperator("+"));


        findViewById(R.id.btnMinus)
                .setOnClickListener(view -> addOperator("-"));


        findViewById(R.id.btnMultiply)
                .setOnClickListener(view -> addOperator("*"));


        findViewById(R.id.btnDivide)
                .setOnClickListener(view -> addOperator("/"));






        // Clear Button

        findViewById(R.id.btnClear).setOnClickListener(view -> {


            expression.setLength(0);


            display.setText("0");


        });






        // Backspace Button

        findViewById(R.id.btnBack).setOnClickListener(view -> {


            if(expression.length() > 0) {


                expression.deleteCharAt(expression.length() - 1);

            }



            if(expression.length() == 0) {


                display.setText("0");


            }

            else {


                display.setText(expression.toString());

            }


        });






        // Equal Button


        findViewById(R.id.btnEqual).setOnClickListener(view -> {



            if(expression.length() == 0) {


                display.setText("0");

                return;

            }




            try {


                double result = calculate(expression.toString());



                String answer;



                if(result == (long) result) {


                    answer = String.valueOf((long) result);


                }

                else {

                    // Round to 8 decimal places to avoid long
                    // floating point tails (e.g. 10/3) overflowing
                    // the display.
                    double rounded = Math.round(result * 1e8) / 1e8;

                    answer = String.valueOf(rounded);


                }




                display.setText(answer);



                expression.setLength(0);

                expression.append(answer);



            }



            catch(Exception e) {



                display.setText("Error");


                expression.setLength(0);



            }



        });



    }







    // Add Operator Safely

    private void addOperator(String operator) {



        if(expression.length() == 0) {

            // Allow a leading minus sign so users can type
            // negative numbers like "-5 + 3". Other operators
            // don't make sense at the very start, so they're
            // still ignored.
            if(operator.equals("-")) {

                expression.append(operator);

                display.setText(expression.toString());

            }

            return;

        }



        char last = expression.charAt(expression.length() - 1);



        if(last == '+' || last == '-' || last == '*' || last == '/') {



            expression.setCharAt(
                    expression.length() - 1,
                    operator.charAt(0)
            );


        }

        else {


            expression.append(operator);


        }



        display.setText(expression.toString());

    }










    // Calculation Engine

    private double calculate(String value) {



        return new Object() {


            int position = -1;

            int ch;



            void nextChar() {


                ch = (++position < value.length())

                        ? value.charAt(position)

                        : -1;


            }





            boolean eat(int charToEat) {



                while(ch == ' ') {


                    nextChar();


                }



                if(ch == charToEat) {


                    nextChar();

                    return true;


                }



                return false;


            }







            double parse() {


                nextChar();


                double x = parseExpression();



                if(position < value.length()) {


                    throw new RuntimeException();


                }



                return x;


            }








            double parseExpression() {


                double x = parseTerm();



                while(true) {


                    if(eat('+')) {


                        x += parseTerm();


                    }


                    else if(eat('-')) {


                        x -= parseTerm();


                    }


                    else {


                        return x;


                    }


                }


            }









            double parseTerm() {



                double x = parseFactor();



                while(true) {



                    if(eat('*')) {



                        x *= parseFactor();



                    }


                    else if(eat('/')) {



                        double divisor = parseFactor();



                        if(divisor == 0) {


                            throw new ArithmeticException();


                        }



                        x /= divisor;



                    }


                    else {


                        return x;


                    }



                }


            }









            double parseFactor() {



                if(eat('+')) {


                    return parseFactor();


                }



                if(eat('-')) {


                    return -parseFactor();


                }



                int start = position;



                while((ch >= '0' && ch <= '9') || ch == '.') {


                    nextChar();


                }




                if(start == position) {


                    throw new RuntimeException();


                }




                return Double.parseDouble(
                        value.substring(start, position)
                );


            }




        }.parse();


    }



}
