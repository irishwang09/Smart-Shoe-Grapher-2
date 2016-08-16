package com.mattmellor.smartshoegrapher;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;

/**
 * Created by Matt Mellor on 8/5/2016.
 * Class that represents a udp wifi client
 * That will accept incoming datagrams(packets)
 * Outer class contains the information about the Udp connection
 *
 * Inner classes are responsible for
 *      1. Pinging the server
 *      2. Reading data from the server
 *
 * Reasoning for this formatting is to avoid having the UI Main thread
 * touch the UDP threads (Avoids errors)
 *
 * Benefits of this approach
 *      1. Scalability
 *          Since each instance of UdpClient will have a separate instance of
 *          threads that ping the server and read the data, code should be scalable to
 *          allow for multiple udp connections at once.
 */

public class UdpClient  {

    private DatagramSocket pingSocket;
    private DatagramSocket receiveSocket;
    private String serverAddress;
    private int remoteServerPort;
    private int localPort;
    private int dataSetsPerPacket;
    public DatagramPacket rcvdPacket;
    private boolean streamData = true;

    /**
     * @param ipAddress : String representing the ip Address/hostname of the remote server
     * @param remoteServerPort : int representing the value of the remote port of the server
     * @param localPort: int representing the value of the local port of the server
     * @param dataSetsPerPacket: int representing the number of data sets per packet
     */
    public UdpClient(String ipAddress, int remoteServerPort, int localPort, int dataSetsPerPacket){
        this.remoteServerPort = remoteServerPort;
        this.serverAddress = ipAddress;
        this.dataSetsPerPacket = dataSetsPerPacket;
        this.localPort = localPort;
    }

    /**
     * Inner class for sending a message to the remote server
     * This is a separate class because all networking actions can't occur
     * on the main UI thread
     */
    public class UdpServerAcknowledge extends Thread{

        private Handler handler;

        public UdpServerAcknowledge(Handler handler){
            this.handler = handler;
        }
        

        /**
         * value to be called by the thread
         */
        public void run(){
            acknowledgeServer();
        }

        private void acknowledgeServer() {
            String mess = "Ping";
            InetAddress address;
            DatagramPacket packet;
            DatagramPacket rPacket;
            byte[] buf = new byte[8];
            boolean fail = false;
            int port = localPort + 1;
            if (localPort == 65535) port = localPort -1;

            try {
                pingSocket = new DatagramSocket(port);
                address = InetAddress.getByName(serverAddress);
                packet = new DatagramPacket(mess.getBytes(), mess.length(), address, remoteServerPort);
                pingSocket.send(packet);
                Log.d("MATT!", "About to wait to receive packet");
                pingSocket.setSoTimeout(500); //2 second wait tile
                rPacket = new DatagramPacket(buf, buf.length);
                pingSocket.receive(rPacket);
                String received = new String(rPacket.getData(), 0, rPacket.getLength());

                if (received.length() > 0){
                    Log.d("MATT!", "Successful Response from server");
                    threadMsg("success");
                }

            }catch(SocketTimeoutException e){
                //Send a message to the fragment
                Log.d("MATT!", "TimeoutException");
                fail = true;
            }catch (SocketException e){
                e.printStackTrace();
                Log.e("MATT!", "socket exception");
                fail = true;
            }catch(UnknownHostException e){
                e.printStackTrace();
                Log.e("MATT!", "unknown host exception");
                fail = true;
            }catch(IOException e) {
                e.printStackTrace();
                Log.e("MATT!", "IOException");
                fail = true;
            }catch(Exception e){
                Log.e("MATT!", "General exception");
                e.printStackTrace();
                fail = true;
            }finally {
                if(fail){
                    threadMsg("fail");
                }
                if(pingSocket != null){
                    pingSocket.close();
                }
            }
        }

        private void threadMsg(String msg) {
            if (!msg.equals(null) && !msg.equals("")) {
                Message msgObj = handler.obtainMessage();
                Bundle b = new Bundle();
                b.putString("message", msg);
                msgObj.setData(b);
                handler.sendMessage(msgObj);
            }
        }
    }


    /**
     * Class for listening to Udp remote server for a long time
     * as a separate thread
     */
    public class UdpDataListener extends Thread {
        //TODO figure out how to store the data for the graph to pick up

        public void run(){
            pingThenListenToServer();
        }

        private void pingThenListenToServer(){
            byte[] buf = new byte[1352]; //TODO calculate this number with a formula
            String received = "";
            InetAddress address;
            String mess = "Android Data Receiver";
            DatagramPacket packet;
            try{
                //Ping the server to tell server IP Address of Android phone
                receiveSocket = new DatagramSocket(localPort);
                address = InetAddress.getByName(serverAddress);
                packet = new DatagramPacket(mess.getBytes(), mess.length(), address, remoteServerPort);
                receiveSocket.send(packet);

                while (streamData) {
                        rcvdPacket = new DatagramPacket(buf, buf.length);
                        receiveSocket.receive(rcvdPacket);
                        received = new String(rcvdPacket.getData(), 0, rcvdPacket.getLength());
                        //String[] val = received.substring(0, received.length() -2).split(",");
                        Log.d("MATT!", received.substring(0, received.length() - 2));
                }
            }catch (SocketException e){
                e.printStackTrace();
                Log.e("MATT!", "socket exception");
            }catch(UnknownHostException e){
                e.printStackTrace();
                Log.e("MATT!", "unknown host exception");
            }catch(IOException e){
                e.printStackTrace();
                Log.e("MATT!", "IOException");
            }catch(Exception e){
                Log.e("MATT!", "General exception");
                e.printStackTrace();
            }finally {
                if(receiveSocket != null){
                    receiveSocket.close();
                }
            }

        }
    }


    //---------------Getter and Setter Methods()------------------

    /**
     * @return InetAddress representing the address of the remote server
     */
    public String getServerAddress() {
        return serverAddress;
    }

    /**
     * @param serverAddress set the value of the remote server address
     *                      must be a InetAddress object
     */
    public void setServerAddress(String serverAddress) {
        this.serverAddress = serverAddress;
    }

    /**
     * @return int remote port of the server
     */
    public int getRemoteServerPort() {
        return remoteServerPort;
    }

    /**
     * @param remoteServerPort set the remote server port
     *                         must be greater than 0
     */
    public void setRemoteServerPort(int remoteServerPort) {
        this.remoteServerPort = remoteServerPort;
    }

    /**
     * @return local port used
     */
    public int getLocalPort() {
        return localPort;
    }

    /**
     * @param localPort to set to use for udp
     *                  must be greater than 0
     */
    public void setLocalPort(int localPort) {
        this.localPort = localPort;
    }

    /**
     * @return int representing the number of data sets per udp packet
     */
    public int getDataSetsPerPacket() {
        return dataSetsPerPacket;
    }

    /**
      * @param dataSetsPerPacket must be greater than 0
     */
    public void setDataSetsPerPacket(int dataSetsPerPacket) {
        this.dataSetsPerPacket = dataSetsPerPacket;
    }

    /**
     *
     * @param streamData
     */
    public void setStreamData(boolean streamData) {
        this.streamData = streamData;
    }
}
