package com.rxleska;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class VisionTrackingClient extends Thread {

    final boolean PRINT_DEBUG = false; // set to true to enable debug messages (should be false in roborio)

    // Client Status and Configuration
    private boolean _isStarted = false;
    private boolean _isConnected = false;
    private int _RPiPort;

    // Vision Status
    private boolean _hasVisionTarget = false;
    private double _targetAngle = 0.0;
    private double _targetDistance = 0.0;
    private long _lastTimestamp = 0;
    private byte[] _lastTrackingImage = null;

    // Socket Programming
    private ServerSocket _serverSocket = null;
    private Socket _clientSocket = null;
    private DataInputStream _in = null;
    private DataOutputStream _out = null;

    public VisionTrackingClient(int RPiPort) {
        _RPiPort = RPiPort;
    }

    public void startVisionTrackingClient() {
        _isStarted = true;
        this.start(); // Start Background Thread, Run will be called
    }

    public void stopVisionTrackingClient() {
        _isStarted = false;
    }

    public boolean isConnected() {
        synchronized (this) {
            return _isConnected;
        }
    }

    public boolean hasVisionTarget() {
        synchronized (this) {
            return _hasVisionTarget;
        }
    }

    public double targetAngle() {
        synchronized (this) {
            return _targetAngle;
        }
    }

    public double targetDistance() {
        synchronized (this) {
            return _targetDistance;
        }
    }

    public long lastTimestamp() {
        synchronized (this) {
            return _lastTimestamp;
        }
    }

    public byte[] lastTrackingImage() {
        synchronized (this) {
            return _lastTrackingImage;
        }
    }

    public void run() {
        while (_isStarted) {
            try {

                boolean connected;
                synchronized (this) {
                    connected = _isConnected;
                }

                if (!connected) {
                    listenForClient();
                }

                processMessages();

            } catch (Exception ex) {
                if (PRINT_DEBUG){
                    System.out.println("Unhandled exception in VisionTrackingClient. " + ex.getMessage());
                }
            }
        }
    }

    protected void listenForClient() throws java.io.IOException {
        if (PRINT_DEBUG) {
            System.out.println(String.format("Initializing Socket on port %d.", _RPiPort));
        }

        _serverSocket = new ServerSocket(_RPiPort, 50, InetAddress.getByAddress(new byte[]{0x00, 0x00, 0x00, 0x00}));
        _serverSocket.setSoTimeout(10000);

        if (PRINT_DEBUG) {
            System.out.println("Waiting for connection.....");
        }

        _clientSocket = _serverSocket.accept();

        if (PRINT_DEBUG) {
            System.out.println("Client connected, Waiting for messages.....");
        }

        _in = new DataInputStream(_clientSocket.getInputStream());
        _out = new DataOutputStream(_clientSocket.getOutputStream());

        synchronized (this) {
            _isConnected = true;
        }
    }

    protected void processMessages() throws java.io.IOException {

        try {
            while (_isStarted) {
                int command = _in.readInt();

                switch (command) {
                    case 1:
                        processMessageType1();
                        break;

                    case 2:
                        processMessageType2();
                        break;

                    case 3:
                        processMessageType3();
                        break;

                    default:
                        if (PRINT_DEBUG) {
                            System.out.println(String.format("Unknown message type id %d", command));
                        }
                        break;
                }
            }
        } catch (Exception ex) {
            System.out.println("Exception occurred while reading. " + ex.getMessage());
        } finally {
            _in.close();
            _out.close();
            _clientSocket.close();

            synchronized (this) {
                _hasVisionTarget = false;
                _isConnected = false;
            }
        }
    }

    protected void processMessageType1() throws java.io.IOException {
        double angle = _in.readDouble(); // 8 Bytes
        double distance = _in.readDouble(); // 8 Bytes
        short hour = _in.readShort(); // 2 bytes
        short min = _in.readShort(); // 2 bytes
        short second = _in.readShort(); // 2 bytes
        int ms = _in.readInt(); // 4 Bytes

        // Calculate timestamp in ms.
        long currentTimestamp = hour * 60 * 60 * 1000 +
                min * 60 * 1000 +
                second * 1000 +
                ms;

        // Determine Time since last target
        if (_lastTimestamp == 0) {
            _lastTimestamp = currentTimestamp;
        }
        long timeSinceLastTargetInMs = currentTimestamp - _lastTimestamp;

        synchronized (this) {
            _lastTimestamp = currentTimestamp;
            _targetAngle = angle;
            _targetDistance = distance;
            _hasVisionTarget = true;
        }

        if (PRINT_DEBUG) {
            System.out.println(String.format("Vision Target: Angle %f, Distance %f, Timestamp %d, Last Target = %d ms", angle, distance, currentTimestamp, timeSinceLastTargetInMs));
        }
    }

    protected void processMessageType2() {
        if (PRINT_DEBUG) {
            System.out.println("No Vision Target");
        }
        synchronized (this) {
            _hasVisionTarget = false;
        }
    }

    protected void processMessageType3() throws java.io.IOException {
        int imageSize = _in.readInt(); // 4 Bytes
        synchronized (this) {
            _lastTrackingImage = new byte[imageSize];
            _in.read(_lastTrackingImage);
        }

        if (PRINT_DEBUG) {
            System.out.println(String.format("Got Vision Image. %d Bytes", imageSize));
        }
    }
}
