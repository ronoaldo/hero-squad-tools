package main

import (
	"gopkg.in/GeertJohan/go.leptonica.v1"
	"gopkg.in/GeertJohan/go.tesseract.v1"
	"log"
	"os"
	"os/exec"
	"time"
)

type img struct {
	src image.Image
}

func (*img) Crop(x, y, w, h int) image.Image {
}

func toPix(i image.Image) *leptonica.Pix {
	b := new(bytes.Buffer)
	if err := png.Encode(b) ; err != nil {
		log.Fatal(err)
	}

}

func main() {
	log.Printf("Hero Squad Tool (beta)")

	log.Printf("Collecting data. Please make sure your phone is connected")
	log.Printf("and listed by adb devices")
	time.Sleep(1 * time.Second)
	squaddump()

	log.Printf("Scanning the images ...")
}

func squaddump() {
	monkey, err := exec.LookPath("monkeyrunner")
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("Executing Monkey Runner")
	cmd := exec.Command(monkey, "squaddump.py")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		log.Fatal(err)
	}
	log.Printf("Monkey runner completed.")
}

func tesseract() {
	tessData := "/usr/share/tesseract-ocr/tessdata"
	lang := "por"
	t, err := tesseract.New(tessdata, lang)
}

func squadparse() {
	
}
