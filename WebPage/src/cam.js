import React, { useState } from "react";
import Webcam from "react-webcam";
import './App.css';
import {
    Card, CardHeader, Button, CardBody, CardFooter, CardText
} from 'reactstrap';
import { isMobile } from 'react-device-detect';

const videoConstraints = {
    width: 640,
    height: 480,
    facingMode: "user"
};

const WebcamComponent = () => {
    const webcamRef = React.useRef(null);
    const [value, setValue] = useState("Result");
    const [dis, setDis] = useState(false);

    const capture = React.useCallback(
        () => {
            setDis(true)
            let imageSrc = webcamRef.current.getScreenshot();
            var unirest = require('unirest');
            unirest('POST', 'https://facemask-apim.azure-api.net/tensorpython37/HttpTrigger1?flag=read')
                .headers({
                    'Ocp-Apim-Subscription-Key': 'APIKEY'
                })
                .send(imageSrc.replace('data:image/jpeg;base64,', ''))
                .end(function (res) {
                    if (res.error) {
                        setValue("No Face Detected, Try Again");
                        setDis(false)
                    }
                    else{
                        setValue(res.raw_body);
                        setDis(false)
                    }
                });
        },
        [webcamRef]
    );

    if (isMobile) {
        return (
            <>
                <Card color="info">
                    <CardHeader className="d-flex justify-content-center">
                        <div style={{ height: "400px" }}>
                            <Webcam
                                style={{ maxWidth: "100%" }}
                                audio={false}
                                height={480}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                                width={640}
                                videoConstraints={videoConstraints}
                            />
                        </div>
                    </CardHeader>
                    <CardBody className="d-flex justify-content-center">
                    <Button color="warning" disabled={dis} style={{ fontSize: "2rem" }} size="lg" onClick={capture}>Capture photo</Button>
                    </CardBody>
                    <CardFooter className="d-flex justify-content-center">
                        <CardText style={{ fontSize: "2rem" }}>{value}</CardText>
                    </CardFooter>
                </Card>
            </>
        );
    }
    else {
        return (
            <>
                <Card color="info" style={{height:"100%"}}>
                    <CardHeader className="d-flex justify-content-center">
                        <div >
                            <Webcam
                                style={{ borderRadius: "10px" }}
                                audio={false}
                                height={480}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                                width={640}
                                videoConstraints={videoConstraints}
                            />
                        </div>
                    </CardHeader>
                    <CardBody className="d-flex justify-content-center">
                        <Button color="warning" disabled={dis} style={{ fontSize: "1.5rem" }} size="lg" onClick={capture}>Capture photo</Button>
                    </CardBody>
                    <CardFooter className="d-flex justify-content-center">
                        <CardText style={{ fontSize: "1.5rem" }}>{value}</CardText>
                    </CardFooter>
                </Card>
            </>
        );
    }
};

export default WebcamComponent;