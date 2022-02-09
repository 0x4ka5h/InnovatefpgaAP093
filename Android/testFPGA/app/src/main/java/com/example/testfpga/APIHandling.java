package com.example.testfpga;

import android.util.Log;

import org.apache.http.entity.StringEntity;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class APIHandling {
    public static String LoginRequest(String username,String password) throws Exception {
        try {
            URL url = new URL("http://192.168.43.217:5000/ownerLogin/?type_=owner&username="+username+"&password="+password);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

//           System.out.println(json);

            System.out.println(url);
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    (conn.getInputStream())));

            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = br.readLine()) != null) {
                response.append(inputLine);
            }
            conn.disconnect();
            JSONObject myResponse = new JSONObject(response.toString());
            try{
                String reason = myResponse.getString("Reason");
                System.out.println(reason);
                return reason;
            }catch (Exception e) {
                return "201";
            }

        }catch(Exception e) {
            return "Error";
        }
    }
    public static String vehicleStatus() throws Exception {
        try {
            URL url = new URL("http://192.168.43.217:5000/api/vehicleStatus");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

//           System.out.println(json);

            System.out.println(url);
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    (conn.getInputStream())));

            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = br.readLine()) != null) {
                response.append(inputLine);
            }
            conn.disconnect();
            JSONObject myResponse = new JSONObject(response.toString());
            try{
                String status= myResponse.getString("status");
                System.out.println(status);
                return status;
            }catch (Exception e) {
                System.out.println(301);
                return "301";
            }

        }catch(Exception e) {
            return "Error";
        }
    }
    public static String requestCamView(String username,String password) throws Exception {
        try {
            URL url = new URL("http://192.168.43.217:5000/ownerLogin/?type_=owner&username="+username+"&password="+password);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

//           System.out.println(json);

            System.out.println(url);
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    (conn.getInputStream())));

            String inputLine;
            StringBuffer response = new StringBuffer();
            while ((inputLine = br.readLine()) != null) {
                System.out.println(inputLine);
                response.append(inputLine);
            }
            conn.disconnect();
            JSONObject myResponse = new JSONObject(response.toString());
            System.out.println("result after Reading JSON Response");
            try{
                String reason = myResponse.getString("reason");
                return reason;
            }catch (Exception e) {
                return "201";
            }

        }catch(Exception e) {
            return "Error";
        }
    }
}