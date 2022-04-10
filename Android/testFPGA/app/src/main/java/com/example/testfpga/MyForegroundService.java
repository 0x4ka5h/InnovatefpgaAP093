package com.example.testfpga;

import android.annotation.SuppressLint;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.IBinder;
import android.util.Base64;
import android.util.Log;
import android.widget.ImageView;

import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

import java.util.Date;

public class MyForegroundService extends Service {
    final String CHANNELID = "ForegroundServiceID";
    Python py = Python.getInstance();
    PyObject pym = py.getModule("backEndRequestCalls");
    String data="";
    Bitmap bmp;
    int count0=0, count1=0,count2 = 0;
    private NotificationManagerCompat notificationManagerCompat;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        new Thread(
                new Runnable() {
                    @Override
                    public void run() {
                        while (true) {
                            try {
                                PyObject isTheft = pym.callAttr("validateThroughNotification", 0);
                                data = isTheft.toString();
                                //System.out.println(getType);
                                if (data != null && data.equals("1") && count0 == 0) {
                                    System.out.println(data);
                                    sendOnChannel("Someone tries to access face lock");
                                    count0 += 1;
                                } else if (data != null && data.equals("0") && count0 == 1) {
                                    count0 = 0;
                                    //cancel notification
                                }


                                PyObject isTowing = pym.callAttr("validateThroughNotification",1);
                                data = isTowing.toString();
                                System.out.println(data);
                                //System.out.println(getType);
                                if (data!=null && data.equals("1")  && count1==0){
                                    System.out.println(data);
                                    //sendOnChannel("Someone tries to lift your vehicle");
                                    count1+=1;
                                }else if (data!=null && data.equals("0") && count1==1){
                                    count1=0;
                                    //cancel notification
                                }


                                PyObject isDeclined = pym.callAttr("validateThroughNotification",2);
                                data = isDeclined.toString();

                                //System.out.println(getType);
                                if (data!=null && data.equals("1")  && count2==0){
                                    System.out.println(data);
                                    //sendOnChannel("A declined person tries to access your vehicle");
                                    count2+=1;
                                }else if (data!=null && data.equals("0") && count2==1){
                                    count2=0;
                                    //cancel notification
                                }
                                Thread.sleep(5000);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                    }
                }
        ).start();
        this.notificationManagerCompat = NotificationManagerCompat.from(this);
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



        return super.onStartCommand(intent, flags, startId);
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    private void sendOnChannel(String text)  {
        Notification notification = null;
        Context context = getApplicationContext();

        Intent notificationIntent = new Intent(context, SuspectCam.class);
        PendingIntent intent_= PendingIntent.getActivity(context, 0,
        notificationIntent, 0);
        Uri soundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        /**try{
            PyObject frame = pym.callAttr("/api/vehicle/DataForNotification/");
            String str_ = frame.toString();
            byte data[] = android.util.Base64.decode(str_, Base64.DEFAULT);
            bmp = BitmapFactory.decodeByteArray(data, 0, data.length);

        }catch(Exception e){
            PyObject frame = pym.callAttr("/api/vehicle/DataForNotification/");
            String str_ = frame.toString();
            byte data[] = android.util.Base64.decode(str_, Base64.DEFAULT);
            bmp = BitmapFactory.decodeByteArray(data, 0, data.length);
        }*/

         //if (data.equals("1")){
         System.out.println(data);
         if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
             notification = new Notification.Builder(this, CHANNELID)
                 .setContentText("HurryUP!")
                 .setContentTitle(text)
             //    .setStyle(new NotificationCompat.BigPictureStyle().bigPicture(bmp))
                 .setAutoCancel(true)
                 .setSmallIcon(R.drawable.redalertuser)
                 .setDefaults(Notification.DEFAULT_SOUND)
                 .setContentIntent(intent_)
                 .setSound(soundUri)
                 .build();
         }
        startForeground(1001, notification);
     }
}