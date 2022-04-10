package com.example.testfpga;

import android.app.Application;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.os.Build;

public class Notifications extends Application  {

    public static final  String CHANNEL_ID = "channel";

    @Override
    public void onCreate() {
        super.onCreate();

        this.createNotificationChannels();
    }

    private void createNotificationChannels()  {
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "Channel",
                    NotificationManager.IMPORTANCE_HIGH
            );
            channel.setDescription("This message is from channel");




            NotificationManager manager = this.getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }
    }
}