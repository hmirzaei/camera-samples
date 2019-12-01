package com.example.android.camera2basic;

import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONObject;

import java.io.DataOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;


public class CallAPI extends AsyncTask<Float, Float, Float> {

    public CallAPI(){
        //set context variables if required
    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
    }

    @Override
    protected Float doInBackground(Float... params) {
        try {
            URL url = new URL("http://192.168.0.19:8000");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            conn.setRequestProperty("Accept","application/json");
            conn.setDoOutput(true);
            conn.setDoInput(true);

            JSONObject jsonParam = new JSONObject();
            jsonParam.put("r", params[0]);
            jsonParam.put("p", params[1]);
            jsonParam.put("y", params[2]);


            Log.i("JSON", jsonParam.toString());
            DataOutputStream os = new DataOutputStream(conn.getOutputStream());
            os.writeBytes(jsonParam.toString());

            os.flush();
            os.close();

            conn.getResponseMessage();
            conn.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return 0f;
    }
}