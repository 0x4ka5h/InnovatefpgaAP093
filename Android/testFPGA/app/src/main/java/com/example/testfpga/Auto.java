package com.example.testfpga;

import android.content.Context;
import android.os.Bundle;
import android.text.InputType;
import android.text.method.HideReturnsTransformationMethod;
import android.text.method.PasswordTransformationMethod;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

public class Auto extends AppCompatActivity {
    int check=0;
    Python py = Python.getInstance();
    PyObject pym = py.getModule("backEndRequestCalls");

    EditText gpsLocation;
    CheckBox previousPath;
    Button done_;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.automode);

        gpsLocation = findViewById(R.id.gpsPoints);
        previousPath = findViewById(R.id.toPreviousGPS);
        done_ = findViewById(R.id.done_);

        previousPath.setOnCheckedChangeListener((button, isChecked) -> {
            if (isChecked) {
                gpsLocation.setText("");
                check = 1;
            }else{
                check = 0;
            }
        });


        done_.setOnClickListener(view ->{
            if (check==1){
                PyObject pyf = pym.callAttr("autoMode");
            }else{
                if(!gpsLocation.getText().equals("")){
                    PyObject pyf = pym.callAttr("autoMode",gpsLocation.getText());
                    System.out.println(gpsLocation.getText());
                }else{
                    Context context = getApplicationContext();
                    int duration = Toast.LENGTH_SHORT;
                    Toast toast = Toast.makeText(context, "Enter GPS coordinates or previous path", duration);
                    toast.show();
                }
            }
        });
    }
}
