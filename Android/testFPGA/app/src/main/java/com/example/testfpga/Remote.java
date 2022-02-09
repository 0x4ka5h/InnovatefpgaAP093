package com.example.testfpga;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Handler;
import android.text.method.Touch;
import android.util.Base64;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.RotateAnimation;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.PopupWindow;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

import java.util.List;

public class Remote extends AppCompatActivity implements View.OnTouchListener {

        ImageView remote_view_;
        ImageView steer_wheel;
        double mCurrAngle = 0;
        double mPrevAngle = 0;
        Button showPopupBtn, closePopupBtn;
        PopupWindow popupWindow;
        LinearLayout linearLayout1;
        private Handler handler = new Handler();
        Python py = Python.getInstance();
        PyObject pym = py.getModule("backEndRequestCalls");
        ImageButton break__, accelarator;
        ImageButton location;

        int steerAngle,breakFunc_,accelaratorFunc_;
        int usLeft_,usRight_,usBack_,speed_;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.remote);

        steer_wheel= findViewById(R.id.steer_angle);
        steer_wheel.setOnTouchListener(this);

        // controls
        break__ = findViewById(R.id.break_);
        break__.setOnClickListener(
                new View.OnClickListener(){
                    @Override
                    public void onClick(View v) {
                        if (breakFunc_ == 0){

                        }
                    }
                }
        );

        accelarator = findViewById(R.id.accelarator);
        /*accelarator.setOnClickListener(
                new View.OnClickListener(){
                    @Override
                    public void onClick(View v) {

                    }
                }

        );*/

        accelarator.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                System.out.println(1);
                return true;
            }
        });
        //location
        location = findViewById(R.id.location);
        location.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                    }
                }
        );

        handler.post(camViewThread);
        handler.post(postControlsThread);
        handler.post(getControlsThread);
    }
    private Runnable camViewThread = new Runnable() {
        @Override
        public void run() {
            PyObject frame = pym.callAttr("camViewByIndex", 2);
            String str_ = frame.toString();
            byte data[] = android.util.Base64.decode(str_, Base64.DEFAULT);
            Bitmap bmp = BitmapFactory.decodeByteArray(data, 0, data.length);
            ((ImageView) findViewById(R.id.remote_view)).setImageBitmap(bmp);
            handler.postDelayed(camViewThread, 25);
        }
    };

    private Runnable postControlsThread = new Runnable() {
        @Override
        public void run() {
            pym.callAttr("remoteCommandsToVehicle",steerAngle,breakFunc_,accelaratorFunc_);
            handler.postDelayed(postControlsThread, 20);
        }
    };

    private Runnable getControlsThread = new Runnable() {
        @Override
        public void run() {
            List<PyObject> controlsDetails = pym.callAttr("retrieveforRC").asList();
            speed_ = controlsDetails.get(0).toInt();
            usLeft_ = controlsDetails.get(1).toInt();
            usRight_ = controlsDetails.get(2).toInt();
            usBack_ = controlsDetails.get(3).toInt();
            handler.postDelayed(getControlsThread, 10);
        }
    };

    // steer wheel rotating animation
    private void animate(double fromDegrees, double toDegrees, long durationMillis) {
        final RotateAnimation rotate = new RotateAnimation((float) fromDegrees, (float) toDegrees,
                RotateAnimation.RELATIVE_TO_SELF, 0.5f,
                RotateAnimation.RELATIVE_TO_SELF, 0.5f);
        rotate.setDuration(durationMillis);
        rotate.setFillEnabled(true);
        rotate.setFillAfter(true);
        if(mCurrAngle<=80 && mCurrAngle>-80) {
            steer_wheel.startAnimation(rotate);
            steerAngle = (int) mCurrAngle;
        }
    }

    @Override
    public boolean onTouch(View v, MotionEvent event) {
        final float xc = steer_wheel.getWidth() / 2;
        final float yc = steer_wheel.getHeight() / 2;

        final float x = event.getX();
        final float y = event.getY();


        mCurrAngle = Math.toDegrees(Math.atan2(x - xc, yc - y));

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN: {
                //steer_wheel.clearAnimation();
                mCurrAngle = Math.toDegrees(Math.atan2(x - xc, yc - y));
                break;
            }
            case MotionEvent.ACTION_MOVE: {
                mPrevAngle = mCurrAngle;
                mCurrAngle = Math.toDegrees(Math.atan2(x - xc, yc - y));
                animate(mPrevAngle, mCurrAngle, 0);
                System.out.println(mCurrAngle);
                break;
            }
            case MotionEvent.ACTION_UP : {
                mPrevAngle = mCurrAngle;
                break;
            }
        }
        return true;
    }

    @Override
    public void onBackPressed() {
        PyObject pyf = pym.callAttr("drivingModes",0,0);
        handler.removeCallbacks(camViewThread);
        handler.removeCallbacks(postControlsThread);
        handler.removeCallbacks(getControlsThread);
        super.onBackPressed();
    }
}
