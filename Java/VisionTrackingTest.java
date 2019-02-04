package com.rxleska;

public class VisionTrackingTest {

    public static void main(String[] args) throws java.lang.InterruptedException {

        System.out.println("RoboRio Vision Tracking Test");
        VisionTrackingClient client = new VisionTrackingClient(5804);
        client.startVisionTrackingClient();

        while(true) {
            Thread.sleep(33);
            if (client.isConnected()) {
                if (client.hasVisionTarget()) {
                    System.out.println(String.format("Target [%d] Angle=%f, Distance=%f", client.lastTimestamp(), client.targetAngle(), client.targetDistance()));
                }
                else {
                    System.out.println("No Vision Target");
                }
            }
        }

        // In real robot when disconnecting the client thread should end cleanly but with the while(true) in this test
        // it can't be called.

        //client.stopVisionTrackingClient();
    }
}
