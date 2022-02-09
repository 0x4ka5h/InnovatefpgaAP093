package com.example.testfpga;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ViewDialog {

    public void showDialog(Activity activity){
        final Dialog dialog = new Dialog(activity);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setCancelable(false);
        dialog.setContentView(R.layout.gpspopup);

        LinearLayout gpsLoaction = (LinearLayout)dialog.findViewById(R.id.gpsLocation);
        gpsLoaction.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Context context = v.getContext();
                dialog.dismiss();
                Intent intent = new Intent(activity, com.example.testfpga.CamView.class);
                //intent.putExtra("Userid", getEmailId);
                context.startActivity(intent);
            }
        });

        LinearLayout gpsTrack = (LinearLayout )dialog.findViewById(R.id.gpsTrack);
        gpsTrack.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {

            }
        });
        LinearLayout gpsPaths = (LinearLayout )dialog.findViewById(R.id.gpsPaths);
        gpsPaths.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {

            }
        });

        dialog.show();

    }
}