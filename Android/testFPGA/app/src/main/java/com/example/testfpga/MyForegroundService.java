package com.example.testfpga;

import android.annotation.SuppressLint;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

import java.util.Date;

public class MyForegroundService extends Service {
    Python py = Python.getInstance();
    PyObject pym = py.getModule("backEndRequestCalls");
    String data="";
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        new Thread(
                new Runnable() {
                    @Override
                    public void run() {
                        while (true) {
                            try {
                                PyObject pyf = pym.callAttr("validateThroughNotification");
                                data = pyf.toString();
                                //need to edit here
                                Thread.sleep(2000);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                    }
                }
        ).start();

        final String CHANNELID = "Foreground Service ID";
        NotificationChannel channel = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            channel = new NotificationChannel(
                    CHANNELID,
                    CHANNELID,
                    NotificationManager.IMPORTANCE_LOW
            );
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            getSystemService(NotificationManager.class).createNotificationChannel(channel);
        }


        /*Intent notificationIntent = new Intent(this, ExampleActivity.class);
        PendingIntent pendingIntent =
                PendingIntent.getActivity(this, 0, notificationIntent, 0);

        Notification notification =
                null;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            notification = new Notification.Builder(this, CHANNELID)
                    .setContentTitle("SomeOne accessed you vehicle! -_- ")
                    .setContentText("HurryUP!")
                    .setSmallIcon(R.drawable.redalertuser)
                    .build();
        }

// Notification ID cannot be 0.
        startForeground(1001, notification);*/



        Notification notification = null;
        if (data.equals("1")){
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                notification = new Notification.Builder(this, CHANNELID)
                        .setContentText("HurryUP!")
                        .setContentTitle("SomeOne accessed you vehicle! ^_^ ")
                        .setSmallIcon(R.drawable.redalertuser)
                        .build();
            }

            //PyObject pyf = pym.callAttr("DataForNotification");
        }else{
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                notification = new Notification.Builder(this, CHANNELID)
                        .setContentText("")
                        .setContentTitle("")
                        .build();
            }

            //PyObject pyf = pym.callAttr("DataForNotification");
        }
        startForeground(1001, notification);

        return super.onStartCommand(intent, flags, startId);
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}