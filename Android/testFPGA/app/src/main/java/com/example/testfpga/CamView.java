package com.example.testfpga;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.Telephony;
import android.util.Base64;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

public class CamView extends AppCompatActivity {
    Python py = Python.getInstance();
    PyObject pym = py.getModule("backEndRequestCalls");
    int Index = 1;
    ImageButton rotateCam;
    Bitmap futureUse;
    private Handler handler = new Handler();
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.camview);

        rotateCam = findViewById(R.id.rotote);
        rotateCam.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (Index == 1) {
                    Index+=1;
                }else{
                    Index=1;
                }
            }
        });

        //(new CheckThread()).start();
        handler.post(runnable);
    }

    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            try{
                PyObject frame = pym.callAttr("camViewByIndex", Index);
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

    /**private class CheckThread extends Thread {
        @Override
        public void run() {
            try {
                changeView();
            }
            catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }
    private void changeView() {
        CamView.this.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                PyObject frame = pym.callAttr("camViewByIndex", Index);
                String str_ = frame.toString();
                System.out.println(str_);
                byte data[] = android.util.Base64.decode(str_, Base64.DEFAULT);
                Bitmap bmp = BitmapFactory.decodeByteArray(data, 0, data.length);
                ((ImageView) findViewById(R.id.imageOfCamView)).setImageBitmap(bmp);
            }
        });
    }*/
}
