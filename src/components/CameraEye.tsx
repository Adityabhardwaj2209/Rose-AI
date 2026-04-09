"use client";

import React, { useRef, useCallback, useImperativeHandle, forwardRef } from "react";
import Webcam from "react-webcam";

export interface CameraEyeHandle {
  capture: () => string | null;
}

const CameraEye = forwardRef<CameraEyeHandle>((_, ref) => {
  const webcamRef = useRef<Webcam>(null);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      return webcamRef.current.getScreenshot();
    }
    return null;
  }, [webcamRef]);

  useImperativeHandle(ref, () => ({
    capture,
  }));

  return (
    <div className="hidden pointer-events-none opacity-0">
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={{
          width: 1280,
          height: 720,
          facingMode: "user",
        }}
      />
    </div>
  );
});

CameraEye.displayName = "CameraEye";

export default CameraEye;
