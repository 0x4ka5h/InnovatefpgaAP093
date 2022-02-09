package com.example.testfpga;

import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageButton;
import android.widget.TextView;
import static com.example.testfpga.APIHandling.vehicleStatus;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

public class Home extends AppCompatActivity {
    ImageButton gpsButton, menuButton, lockButton, unlockButton, powerButton;
    ImageButton remoteButton, autoButton, cameraButton;
    TextView statusUpdate;
    Python py = Python.getInstance();
    PyObject pym = py.getModule("backEndRequestCalls");
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home);
        statusUpdate = (TextView) findViewById(R.id.statusBar);
        try {
            PyObject pyf = pym.callAttr("vehicleStatus");
            String status = pyf.toString();
            if (!status.equals("301")){
                statusUpdate.setText(status);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }


        gpsButton =(ImageButton)findViewById(R.id.gps);
        gpsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ViewDialog alert = new ViewDialog();
                alert.showDialog(Home.this);
            }
        });
        menuButton =(ImageButton)findViewById(R.id.log);
        menuButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });
        lockButton =(ImageButton)findViewById(R.id.lock);
        lockButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {



            }
        });
        unlockButton =(ImageButton)findViewById(R.id.unlock);
        unlockButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });
        powerButton =(ImageButton)findViewById(R.id.power);
        powerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });


        cameraButton =(ImageButton)findViewById(R.id.camera);
        cameraButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PyObject pyf = pym.callAttr("drivingModes",0,1);

                Intent intent = new Intent(Home.this, CamView.class);
                //intent.putExtra("Userid", getEmailId);
                startActivity(intent);
            }
        });


        autoButton =(ImageButton)findViewById(R.id.auto);
        autoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PyObject pyf = pym.callAttr("drivingModes",2,0);
                Intent intent = new Intent(Home.this, Auto.class);
                //intent.putExtra("Userid", getEmailId);
                startActivity(intent);
            }
        });


        remoteButton =(ImageButton)findViewById(R.id.remote);
        remoteButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PyObject pyf = pym.callAttr("drivingModes",1,2);
                Intent intent = new Intent(Home.this, Remote.class);
                startActivity(intent);
            }
        });

    }
}