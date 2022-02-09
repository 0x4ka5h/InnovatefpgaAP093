package com.example.testfpga;

import static com.example.testfpga.APIHandling.LoginRequest;
//import static com.example.testfpga.APIHandling.homeURLRequest;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Parcelable;
import android.os.StrictMode;
import androidx.appcompat.app.AppCompatActivity;
import android.text.InputType;
import android.text.method.HideReturnsTransformationMethod;
import android.text.method.PasswordTransformationMethod;
import android.util.Log;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;


public class MainActivity extends AppCompatActivity {
    Python py = Python.getInstance();
    PyObject pym = py.getModule("backEndRequestCalls");

    Button loginButton;
    EditText emailid,password;
    CheckBox show_hide_password;
    String loginCode;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE); //will hide the title
        setContentView(R.layout.activity_main);
        //hide the title bar
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();

        StrictMode.setThreadPolicy(policy);

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));

        }

        loginButton = findViewById(R.id.loginBtn);
        emailid = findViewById(R.id.login_emailid);
        password = findViewById(R.id.login_password);
        show_hide_password = findViewById(R.id.show_hide_password);

        show_hide_password.setOnCheckedChangeListener((button, isChecked) -> {
            if (isChecked) {
                show_hide_password.setText(R.string.hide_pwd);
                password.setInputType(InputType.TYPE_CLASS_TEXT);
                password.setTransformationMethod(HideReturnsTransformationMethod
                        .getInstance());
            } else {
                show_hide_password.setText(R.string.show_pwd);
                password.setInputType(InputType.TYPE_CLASS_TEXT
                        | InputType.TYPE_TEXT_VARIATION_PASSWORD);
                password.setTransformationMethod(PasswordTransformationMethod
                        .getInstance());
            }
        });

        loginButton.setOnClickListener(v -> {
            String getEmailId = emailid.getText().toString();
            String getPassword = password.getText().toString();


            try {
                PyObject pyf = pym.callAttr("ownerLogIn",getEmailId,getPassword);
                loginCode = pyf.toString();
                System.out.println(loginCode);
                //loginCode.text = loginCode.toString();
                //loginCode = LoginRequest(getEmailId,getPassword);
            } catch (Exception e) {
                e.printStackTrace();
                //Log.d("message- ",e.printStackTrace());
            }
            Context context = getApplicationContext();
            int duration = Toast.LENGTH_SHORT;

            if (loginCode!=null && loginCode.equals("201")) {
                Toast toast = Toast.makeText(context, "Login Successful", duration);
                toast.show();
                Intent intent = new Intent(MainActivity.this, com.example.testfpga.Home.class);
                startActivity(intent);
                finish();
            }else {
                Toast toast = Toast.makeText(context, loginCode, duration);
                toast.show();
            }
        });
    }
}
