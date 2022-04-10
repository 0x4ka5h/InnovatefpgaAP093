package com.example.testfpga;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.Telephony;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

public class SuspectCam extends AppCompatActivity {
    Python py = Python.getInstance();
    PyObject pym = py.getModule("backEndRequestCalls");
    int Index = 1;
    Button accept;
    Button decline;
    Bitmap futureUse;
    private Handler handler = new Handler();
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.suspectview);

        accept = findViewById(R.id.accept);
        accept.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                pym.callAttr("acceptORdecline", 1);
            }
        });

        decline = findViewById(R.id.decline);
        decline.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                pym.callAttr("acceptORdecline", 0);
            }
        });

        //(new CheckThread()).start();
        handler.post(runnable);
    }

    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            try{
                PyObject frame = pym.callAttr("camViewByIndex", 1);
                String str_ = frame.toString();
                byte data[] = android.util.Base64.decode(str_, Base64.DEFAULT);
                Bitmap bmp = BitmapFactory.decodeByteArray(data, 0, data.length);
                ((ImageView) findViewById(R.id.imageOfCamView)).setImageBitmap(bmp);
                handler.postDelayed(runnable, 20);
                futureUse = bmp;

            }catch(Exception e){

                ((ImageView) findViewById(R.id.imageOfCamView)).setImageBitmap(futureUse);
                handler.postDelayed(runnable, 20);
            }

        }
    };

    @Override
    public void onBackPressed() {
        PyObject pyf = pym.callAttr("drivingModes",0,0);
        handler.removeCallbacks(runnable);
        super.onBackPressed();
    }

}
