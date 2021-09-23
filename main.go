package main

import (
	"errors"
	"image/color"
	"io"
	"io/ioutil"
	"os"
	"strconv"

	"bufio"
	"encoding/csv"
	"fmt"
	"log"
	"strings"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
	"gonum.org/v1/plot/vg/draw"
	"gonum.org/v1/plot/vg/vgimg"
)

func main() {

	files, err := ioutil.ReadDir(".")
	if err != nil {
		log.Fatal(err)
	}
	filefound := false
	for _, f := range files {
		if f.Name() == "input.csv" {
			filefound = true
			break
		}
	}
	if !filefound {
		fmt.Println("Нет input.csv файла")

		fmt.Print("Press 'Enter' to continue...")
		bufio.NewReader(os.Stdin).ReadBytes('\n')
		log.Fatal("Нет input.csv файла")

	}

	fmt.Println("input.csv открыт")

	try2 := readFileConverToString("input.csv")

	r := csv.NewReader(strings.NewReader(try2))
	r.Comma = ';'
	r.Comment = '#'

	records, err := r.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	values := valuesFromColumn(records, 0)

	fmt.Println("Введите количество разбиений гистограммы:\t")
	var num_bins int
	_, err = fmt.Scanf("%d", &num_bins)

	if err != nil {
		log.Println("num_bins string error:\n", err)
		num_bins = 10
	}

	//	num_bins := 10

	err = histPlot(values, num_bins)
	if err != nil {
		log.Println("hist calc+plot error:\n", err)
	}

	fmt.Print("Press 'Enter' to continue...")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
	bufio.NewReader(os.Stdin).ReadBytes('\n')
}

func readFileConverToString(name string) string {
	f, err := os.Open(name)
	if err != nil {
		log.Fatalf("unable to read file: %v", err)
	}
	defer f.Close()
	stat, err := f.Stat()
	if err != nil {
		log.Fatalf("Error analyzing file: %v", err)
	}
	fmt.Println("Размер файла ", name, " равен ", stat.Size(), " байт")
	buf := make([]byte, stat.Size()*2)

	for {
		n, err := f.Read(buf)
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Printf("Warning while reading file: %v", err)
			continue
		}
		if n > 0 {
			//fmt.Printf("buf[:n]:\t%v\n what is", string(buf[:n]))
			return string(buf[:n])
		}
		//		fmt.Println("iter")
	}
	fmt.Printf("Somethig went wrong with file, empty data expected")
	return ""
}

func valuesFromColumn(records [][]string, col int) plotter.Values {
	var values plotter.Values

	for _, j := range records {

		feetFloat, err := strconv.ParseFloat(strings.TrimSpace(j[col]), 64)
		if err == nil {
			values = append(values, feetFloat)
		}

	}
	return values

}

func histPlot(values plotter.Values, num_bins int) error {

	histncount, _ := plotter.NewHist(values, num_bins)
	histvolu, err := plotter.NewHist(values, num_bins)
	if err != nil {
		panic(err)
	}

	p := plot.New()
	p.Title.Text = "Гистограммы размеров микросфер"
	p.X.Label.Text = "d, мкм"
	p.Y.Label.Text = "P_n, %"

	//	fmt.Println("histncount:\t", histncount)
	//	fmt.Println("histncount.Bins:\t", histncount.Bins)

	totWidth := histncount.Width * float64(num_bins) * 100
	if totWidth <= 0 {
		log.Fatalf("totWidth <= 0")
	}
	histncount.Normalize(totWidth / float64(num_bins))

	xzz := len(histvolu.Bins)
	for i := 0; i < xzz; i++ {

		dia := (histncount.Bins[i].Min + histncount.Bins[i].Max) / 2.0
		dia3 := dia * dia * dia
		weighted := dia3 * histncount.Bins[i].Weight
		histvolu.Bins[i] = plotter.HistogramBin{Min: histncount.Bins[i].Min, Max: histncount.Bins[i].Max, Weight: weighted}
	}
	histvolu.Normalize(totWidth / float64(num_bins))
	fmt.Println("\nКоличественная гистограмма (границы диапазонов и вероятность):\n", histncount.Bins)
	fmt.Println("\nОбъемная гистограмма (границы диапазонов и вероятность):\n", histvolu.Bins)

	ave, err := calcAverDia(histncount.Bins)
	if err != nil {
		return err
	}
	fmt.Println("Средний диаметр количественной гистограммы:\t", ave, "\tмкм")

	ave, err = calcAverDia(histvolu.Bins)
	if err != nil {
		return err
	}
	fmt.Println("Средний диаметр объемной гистограммы:\t", ave, "\tмкм")

	c := vgimg.New(vg.Points(120), vg.Points(100))
	dc := draw.New(c)

	//	red := exampleThumbnailer{Color: color.NRGBA{R: 255, A: 255}}	//green := exampleThumbnailer{Color: color.NRGBA{G: 255, A: 255}}	//	blue := exampleThumbnailer{Color: color.NRGBA{B: 255, A: 255}}
	gray := exampleThumbnailer{Color: color.Gray{Y: 128}, linecolor: color.Black}
	trans := exampleThumbnailer{Color: color.Transparent, linecolor: color.NRGBA{R: 255, A: 255}}

	l := plot.NewLegend()
	l.Padding = vg.Millimeter
	l.YPosition = draw.PosCenter

	l.Add("Объемное распределение", gray)
	histvolu.Color = gray.linecolor //color.RGBA{R: 255, A: 255}
	histvolu.FillColor = gray.Color
	l.Add("Количественное распределение", trans)
	histncount.Color = trans.linecolor
	histncount.FillColor = trans.Color

	// purpleRectangle draws a purple rectangle around the given Legend.
	purpleRectangle := func(l plot.Legend) {
		r := l.Rectangle(dc)
		dc.StrokeLines(draw.LineStyle{
			Color: color.NRGBA{R: 255, B: 255, A: 255},
			Width: vg.Points(1),
		}, []vg.Point{
			{X: r.Min.X, Y: r.Min.Y}, {X: r.Min.X, Y: r.Max.Y}, {X: r.Max.X, Y: r.Max.Y},
			{X: r.Max.X, Y: r.Min.Y}, {X: r.Min.X, Y: r.Min.Y},
		})
	}

	l.Draw(dc)
	purpleRectangle(l)

	l.Left = true
	l.Top = true
	l.Draw(dc)
	purpleRectangle(l)

	p.Legend = l
	p.Add(histvolu)
	p.Add(histncount)
	p.X.Min = 0
	p.X.Max *= 1.2
	p.Y.Min = 0
	p.Y.Max *= 1.2

	if err := p.Save(10*vg.Centimeter, 10*vg.Centimeter, "hist_n_count.png"); err != nil {
		fmt.Println("Error saving png:", err)
		panic(err)
	}
	return nil
}

func calcAverDia(bins []plotter.HistogramBin) (float64, error) {
	var aver, sum float64
	xzz := len(bins)
	for i := 0; i < xzz; i++ {

		dia := (bins[i].Min + bins[i].Max) / 2.0
		sum += bins[i].Weight
		aver += bins[i].Weight * dia
	}
	if sum <= 0 {
		return 0, errors.New("aver dia division by 0")
	}
	return (aver / sum), nil
}

type exampleThumbnailer struct {
	color.Color
	linecolor color.Color
}

// Thumbnail fulfills the plot.Thumbnailer interface.
func (et exampleThumbnailer) Thumbnail(c *draw.Canvas) {
	pts := []vg.Point{
		{X: c.Min.X, Y: c.Min.Y},
		{X: c.Min.X, Y: c.Max.Y},
		{X: c.Max.X, Y: c.Max.Y},
		{X: c.Max.X, Y: c.Min.Y},
	}
	poly := c.ClipPolygonY(pts)
	c.FillPolygon(et.Color, poly)

	pts = append(pts, vg.Point{X: c.Min.X, Y: c.Min.Y})
	outline := c.ClipLinesY(pts)
	c.StrokeLines(draw.LineStyle{
		Color: et.linecolor, //color.Black,
		Width: vg.Points(1),
	}, outline...)
}
