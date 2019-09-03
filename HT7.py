# TIE - 02100, HT7
# Pokeripeli
# Tehnyt: Jaakko Huusko

from tkinter import *
from tkinter.messagebox import askyesno
import random
# import Images ,kansio jossa on korttien kuvat
import time
from winsound import PlaySound

class GUI:

    def __init__(self):
        """
        Käyttöliittymän rakentaja.
        :param self.__mainwindow: käyttöliittymän pääikkuna
        :param self.__korttikuvat: korttien kuvat listassa
        :param self.__tarkistus: luo tarkistus dictin, jossa avaimena kortin
        kuvanumero ja vastauksena kortin arvo ja maa.
        :param self.__Korttipakka: korttipakka, jossa 54 korttia (2 jokeria)
        :param self.__valitseArvot: 'lukitse'-nappien arvot, joita muuttamalla
        kortit lukitaan tai poistetaan lukituksesta
        :param self.__extrajokerit: pelaajan ostamien lisäjokereiden lukumäärä
        :param self.__jokeriteksti:kirjoittaa pääikkunaan lisäjokereiden määrän
        :param self.__jokerihinta: lisäjokerin hinta (pistettä)
        :param self.__jokerihintaVar: lisäjokerin hinnan tekstimuuttuja
        :param self.__teksti: tekstimuuttuja
        :param self.__tulos: pelaajan kokonaispisteet
        :param self.__pelimerkit: pelaajan pelimerkkien määrä
        :param self.__panos: pelaajan panos
        :param self.__m.... : tuloksen, pelimerkkien ja panoksen teksimuuttujat
        :param self.__TOP10: entry, johon pelaaja kirjoittaa nimimerkkinsä
        :param self.__TOP10ruutu: ikkuna joka tulee näytölle pelin päätyttyä
        :param self.__jakonappi: jakonappi
        :param self.__tekstiLabel: label, johon 'self.__teksti' -muuttujaan
        kirjoitettu teksti ilmestyy
        :param self.__pelikortit: lista, joka sisältää kaikki korttimuuttujat

        Kehitettävää: kuvien ja äänien tuonti kansioista
        """
# muuttujat
        self.__mainwindow = Tk()
        self.__mainwindow.title("Pokeripeli")
        self.__mainwindow.resizable(width=FALSE, height=FALSE)
        self.__korttikuvat = []

        for i in range(101, 156):
            kuvatiedosto = str(i)+".gif"
            kuva = PhotoImage(file=kuvatiedosto)
            self.__korttikuvat.append(kuva)

        self.__tarkistus = {}
        self.luo_tarkistus()

        self.__Korttipakka = []
        for i in range(54):
            self.__Korttipakka.append(i)

        self.__valitseArvot = []
        for i in range(5):
            self.__valitseArvot.append(0)
        self.__extrajokerit = 0
        self.__jokeriteksti = StringVar()
        self.__jokeriteksti.set("Lisäjokereita: {}".format(self.__extrajokerit))
        self.__jokerihinta = 5000
        self.__jokerihintaVar = StringVar()
        self.__jokerihintaVar.set("Osta lisäjokeri: (5k)")
        self.__teksti = StringVar()
        self.__tulos = 0
        self.__pelimerkit = 100
        self.__panos = int(self.__pelimerkit * 0.1)
        self.__panosMAX = 0
        self.__mpanos = StringVar()
        self.__mpanos.set("Panos: " + str(self.__panos))
        self.__mpelimerkit = StringVar()
        self.__mpelimerkit.set("Pelimerkit: " + str(self.__pelimerkit))
        self.__mtulos = StringVar()
        self.__mtulos.set("Pisteet: " + str(self.__tulos))
        self.__top10 = Entry
        self.__top10ruutu = Tk
# napit
        Button(self.__mainwindow, text="Uusi peli", font=10,
            command=self.uusi_peli_kysymys).grid(row=0, sticky= W+E+S+N)
        Button(self.__mainwindow, text="Ohjeet",font=10, command=self.ohjeet) \
            .grid(row=1, sticky= W+E+S+N)
        Button(self.__mainwindow, text="TOP 10", font=10, command=self.tulokset)\
            .grid(row=2, sticky= W+E+S+N)
        Button(self.__mainwindow, text="Voittotaulukko", font=10,
               command=self.voittotaulukko).grid(row=3, sticky= W+E+S+N)
        Button(self.__mainwindow, textvariable=self.__jokerihintaVar, font=10,
               command=self.osta_jokeri).grid(row=4, sticky= W+E+S+N)
        self.__jakonappi = Button(self.__mainwindow, text="Jaa", bg="lightblue",
                                  command=self.pelaa, state= DISABLED)
        self.__jakonappi.grid(row=7, column=5, sticky= W+E+N+S, pady=10)
        Button(self.__mainwindow, text="Lopeta", font=10, command=self.lopeta)\
        .grid(row=8,sticky= W+E)
        self.__panosMAXButton = Button(self.__mainwindow, text="Panosta kaikki",
                                    fg="pink",bg="grey",command=self.max_panos)
# lukitse -napit
        for i in range(5):
            Button(self.__mainwindow,text="Lukitse",bg="lightgreen" ,
                   state = DISABLED, command=lambda: self.lukitse(i+1)) \
            .grid(row=4, column=i+1,rowspan=3,padx=10,sticky=W+E)

# Labelit
        Label(self.__mainwindow, text=" "*10).grid(row = 0, column=8,sticky=W+E)
        Label(self.__mainwindow, textvariable=self.__mpanos,font=10)\
        .grid(row = 0, column=3, sticky=W)
        Label(self.__mainwindow, textvariable=self.__mpelimerkit,font=10)\
        .grid(row = 0, column=4, sticky=W+E, columnspan=3)
        Label(self.__mainwindow, textvariable=self.__mtulos,font=10)\
        .grid(row = 0, column=1, sticky=W+E, columnspan=2,)
        self.__tekstiLabel = Label(self.__mainwindow,
                                   textvariable=self.__teksti)
        self.__tekstiLabel.grid(row=7,column=1,columnspan=3)
        Label(self.__mainwindow, textvariable=self.__jokeriteksti)\
            .grid(row=5, column=0)
# Kuvamuuttujien luonti
        self.__kortti1 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti1.grid(row=1, column=1, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti2 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti2.grid(row=1, column=2, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti3 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti3.grid(row=1, column=3, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti4 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti4.grid(row=1, column=4, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti5 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti5.grid(row=1, column=5, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__pelikortit = [self.__kortti1,self.__kortti2,self.__kortti3,
                             self.__kortti4,self.__kortti5]

        self.__mainwindow.mainloop()

    def lopeta(self):
        """
        Kysyy haluaako pelaaja varmasti lopettaa pelaamisen. Ilmoittaa, että
        pelaajan pisteitä ei tallenneta, jos peli on vielä kesken.
        """
        if self.__pelimerkit != 0:
            vastaus = askyesno(title="Lopeta",
                               message="Haluatko varmasti lopettaa?\n"
                                        "Nykyisiä pisteitäsi ei tallenneta")
        else:
            vastaus = askyesno(title="Lopeta",
                               message="Haluatko varmasti lopettaa?")
        if vastaus == True:
            self.__mainwindow.destroy()
            return False

    def uusi_peli_kysymys(self):
        """
        Kysyy haluaako pelaaja varmasti aloittaa uuden pelin ja ilmoittaa, että
        pelaajan pisteitä ei tallenneta, jos peli on vielä kesken.
        """
        if self.__pelimerkit != 0:
            vastaus = askyesno(title="Uusi peli",
                            message="Haluatko varmasti aloittaa uuden pelin?\n"
                                    "Nykyisiä pisteitäsi ei tallenneta")
        else:
            vastaus = askyesno(title="Uusi peli",
                            message="Haluatko aloittaa uuden pelin?")

        if vastaus == True:
            self.uusi_peli()

    def uusi_peli(self):
        """
        Alustaa uuden pelin.
        """
        PlaySound("uusi_peli.wav",1)
        self.__teksti.set("Onnea peliin!")
        self.__extrajokerit = 0
        self.alusta_korttipakka()
        for i in range(5):
            self.alusta_napit(i)
        self.__jakonappi = Button(self.__mainwindow, text="Jaa",bg="lightblue",
                                  command=self.pelaa)
        self.__jakonappi.grid(row=7,column=5, sticky= W+E+N+S, pady=10)
        self.__tulos = 0
        self.__panosMAX = 0
        self.__pelimerkit = 100
        self.__panos = int(self.__pelimerkit*0.1)
        self.__mpanos.set("Panos: " + str(self.__panos))
        self.__mpelimerkit.set("Pelimerkit: " + str(self.__pelimerkit))
        self.__mtulos.set("Pisteet: " + str(self.__tulos))
        self.__top10ruutu = Tk
        self.__top10 = Entry
        self.__kortti1 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti1.grid(row=1, column=1, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti2 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti2.grid(row=1, column=2, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti3 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti3.grid(row=1, column=3, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti4 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti4.grid(row=1, column=4, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__kortti5 = Label(self.__mainwindow, image=self.__korttikuvat[54],
                               anchor=N)
        self.__kortti5.grid(row=1, column=5, rowspan=3,
                                    padx=10, sticky=W+E+S+N)
        self.__pelikortit = [self.__kortti1,self.__kortti2,self.__kortti3,
                             self.__kortti4,self.__kortti5]

    def pelaa(self):
        """
        Jakaa näytölle viisi satunnaista korttia ja lisää nykyisten pelimerk-
        kien määrän pisteisiin.
        Aktivoi 'lukitse'-napit
        Epäaktivoi lisäjokerin ostomahdollisuuden
        Muuttaa 'jaa'-napin 'vaihda'-napiksi
        """
        if self.__panosMAX ==2:
            self.__panos = self.__pelimerkit
        self.alusta_korttipakka()
        Button(self.__mainwindow, textvariable=self.__jokerihintaVar,
               state=DISABLED, font=10, command=self.osta_jokeri)\
            .grid(row=4, sticky= W+E+S+N)
        self.__teksti.set("")

        if self.__panosMAX > 0:
            self.__panosMAXButton.grid_remove()

        for i in range(5):
            Button(self.__mainwindow,text="Lukitse",bg="lightgreen",
                   command=lambda: self.lukitse(i+1)) \
            .grid(row=4, column=i+1,rowspan=3,padx=10,sticky=W+E)

        for i in range(5):
            self.alusta_napit(i)

        Button(self.__mainwindow, text="Lopeta",font=10, command=self.lopeta) \
            .grid(row=8,sticky= W+E)

        self.__tulos += self.__pelimerkit
        self.__mtulos.set("Pisteet: {}"
                          .format(self.muuta_lukuasua(self.__tulos)))
        self.__pelimerkit -= self.__panos
        self.__mpelimerkit.set("Pelimerkit: {}"
                               .format(self.muuta_lukuasua(self.__pelimerkit)))
        self.__mpanos.set("Panos: {}"
                          .format(self.muuta_lukuasua(self.__panos)))
        self.__mainwindow.update_idletasks()

        for i in range(5):
            PlaySound("kortti.wav",1)
            self.__pelikortit[i]["image"] = self.__korttikuvat[54]
            self.__mainwindow.update_idletasks()
            time.sleep(0.05)

        for i in range(5):
            luku = self.__Korttipakka[random.randint(0,len(self.__Korttipakka)-1)]
            self.__pelikortit[i]["image"] = self.__korttikuvat[luku]
            self.__Korttipakka.remove(luku)
            self.__mainwindow.update_idletasks()
            time.sleep(0.05)

        self.__jakonappi = Button
        self.__vaihtonappi = Button(self.__mainwindow, text="Vaihda",
                                    bg="lightblue",command=self.vaihda)
        self.__vaihtonappi.grid(row=7,column=5, sticky= W+E+N+S, pady=10)

    def vaihda(self):
        """
        Toteuttaa lukittujen korttien vaihdon ja kutsuu 'tarkista_voitto'-funk-
        tiota, kun kortit on vaihdettu. Jos pelaajan pelimerkit menevät nollaan
        kutsuu 'lopetus'-funktiota.
        Aktivoi lisäjokerin ostomahdollisuuden.
        Epäaktivoi 'lukitse'-napit
        Muuttaa 'vaihda'-napin 'jaa'-napiksi
        """
        Button(self.__mainwindow, textvariable=self.__jokerihintaVar, font=10,
               command=self.osta_jokeri).grid(row=4, sticky= W+E+S+N)
        for i in range(5):
            if self.__valitseArvot[i]%2 == 0:
                PlaySound("kortti.wav",1)
                self.__pelikortit[i]["image"] = self.__korttikuvat[54]
                self.__mainwindow.update_idletasks()
                time.sleep(0.05)

        for i in range(5):
            luku = self.__Korttipakka[random.randint(0,len(self.__Korttipakka)-1)]
            if self.__valitseArvot[i]%2 == 0:
                self.__pelikortit[i]["image"] = self.__korttikuvat[luku]
                self.__Korttipakka.remove(luku)
                self.__mainwindow.update_idletasks()
                time.sleep(0.05)

        self.tarkista_voitto()
        self.__vaihtonappi = Button
        self.__jakonappi = Button(self.__mainwindow, text="Jaa",bg="lightblue",
                                  command=self.pelaa)
        self.__jakonappi.grid(row=7,column=5, sticky= W+E+N+S, pady=10)

        for i in range(5):
            self.alusta_napit(i)
        self.alusta_korttipakka()

        for i in range(5):
            Button(self.__mainwindow,text="Lukitse",bg="lightgreen",
                   state=DISABLED, command=lambda: self.lukitse(i+1)) \
            .grid(row=4, column=i+1,rowspan=3,padx=10,sticky=W+E)

        if self.__pelimerkit == 0:
            self.__teksti.set("Peli päättyi!")
            self.lopetus()

        #Arpoo numeron 0-10 väliltä ja jos numero on 1 luo panosMAX -napin
        if self.__pelimerkit != 0:
            i = random.randint(0,10)
            if i == 1:
                self.__panosMAXButton.grid(row=7,column=4,sticky=W+E)
                self.__panosMAX += 1

    def max_panos(self):
        """
        Muuttaa pelaajan panoksen pelimerkkien suuruiseksi.
        """
        PlaySound('max_panos.wav',1)
        self.__panosMAX += 1
        self.__mpanos.set("Panos: {}"
                          .format(self.muuta_lukuasua(self.__pelimerkit)))

    def lopetus(self):
        """
        Kun pelaajan pelimerkit loppuvat, toteutetaan tämä funktio. Luo ikkunan
        johon pelaaja syöttää nimimerkkinsä. Jos pelaajan pisteet ovat
        tarpeeksi hyvät, pääsee hän TOP-10 listalle.

        Kehitettävää: kysyy pelaajan nimimerkkiä ainoastaan silloin, kun pelaa-
        jan pisteet riittävät TOP-10 listalle.
        Kehitettävää: rajaa pelaajan nimimerkin tietyn pituiseksi
        """
        PlaySound('lopetus.wav',1)
        self.__jakonappi = Button(self.__mainwindow, text="Jaa",bg="lightblue"
                                  ,state=DISABLED, command=self.pelaa)
        self.__jakonappi.grid(row=7,column=5, sticky= W+E+N+S, pady=10)
        self.__top10ruutu = self.__top10ruutu()
        self.__top10ruutu.title("Peli päättyi")
        Label(self.__top10ruutu,text="Syötä nimimerkkisi:")\
            .grid(row=0, column=0, columnspan=2, sticky=W+E)
        self.__top10 = self.__top10(self.__top10ruutu)
        self.__top10.grid(row=1, column=0, sticky=W+E)
        self.__top10.bind('<Return>',self.enter)
        okButton = Button(self.__top10ruutu, text="OK", command=self.lue_syöte)
        okButton.grid(row=1, column=1)

    def enter(self, event):
        self.lue_syöte()

    def lue_syöte(self):
        """
        Lukee pelaajan näppäilemän nimimerkin ja kirjoittaa sen 'tulokset.txt'-
        tiedostoon.
        """
        nimi = self.__top10.get()
        lue = open("tulokset.txt", mode="r")
        lista = []
        for rivi in lue:
            lista.append(rivi)
        tiedosto = open("tulokset.txt",mode="w")
        for rivi in lista:
            tiedosto.write(rivi)
        tiedosto.write("\n")
        tiedosto.write("{}:{}".format(nimi, int(self.__tulos)))
        tiedosto.close()
        self.__top10ruutu.destroy()
        self.tulokset()

    def ohjeet(self):
        """
        Luo ikkunan, josta näkyy pelin ohjeet. Ohjeet luetaan tiedostosta:
        'ohjeet.txt'.
        """
        ruutu = Tk()
        ruutu.title("Ohjeet")
        teksti = open("ohjeet.txt", mode ="r")
        ohjeet = ""
        for rivi in teksti:
            ohjeet += rivi
        Label(ruutu, text=ohjeet).grid(row=0)
        Button(ruutu,text="Palaa",command=ruutu.destroy).grid(row=1,pady=10)

    def tulokset(self):
        """
        Luo uuden ikkunan josta näkee TOP 10-pelaajat. Lukee tiedot tiedostosta
        'tulokset.txt'.
        """
        ruutu = Tk()
        ruutu.title("TOP 10")
        tulokset = []
        teksti = open("tulokset.txt", mode ="r")
        for rivi in teksti:
            rivi = rivi.split(":")
            tulokset.append(rivi)
        tulokset = sorted(tulokset, key= lambda a:int(a[1]), reverse=True)
        nimi = ""
        pisteet = ""
        laskuri = 0
        for rivi in tulokset[:10]:
            laskuri += 1
            nimi += str(laskuri)+". " + rivi[0].rstrip().lstrip() +"\n"
            pisteet += rivi[1].rstrip().lstrip() +"\n"
        Label(ruutu, text=nimi).grid(row =0, column=0, sticky=W+S+N,padx=10)
        Label(ruutu, text=pisteet).grid(row=0, column = 1, sticky=E+S+N)
        Button(ruutu,text="Palaa",command=ruutu.destroy, anchor=CENTER)\
            .grid(row=1,columnspan= 2, pady=10)

    def voittotaulukko(self):
        """
        Luo ikkunan, johon kirjoittaa 'voittotaulukko.txt' tiedoston rivit.
        """
        ruutu = Tk()
        ruutu.title("TOP 10")
        tulokset = []
        teksti = open("voittotaulukko.txt", mode ="r")
        for rivi in teksti:
            rivi = rivi.split(":")
            tulokset.append(rivi)
        tulokset = sorted(tulokset, key= lambda a:int(a[1]), reverse=True)
        nimi = ""
        pisteet = ""
        for rivi in tulokset[:10]:
            nimi +=rivi[0].rstrip().lstrip() +"\n"
            pisteet += rivi[1].rstrip().lstrip() +"\n"
        Label(ruutu, text=nimi).grid(row =0, column=0, sticky=W+S+N,padx=10)
        Label(ruutu, text=pisteet).grid(row=0, column = 1, sticky=E+S+N)
        Button(ruutu,text="Palaa",command=ruutu.destroy,anchor=CENTER)\
            .grid(row=1,columnspan= 2, pady=10)

    def lukitse(self,numero):
        """
        Lukitsee pelaajan valitseman kortin. Muuttaa napin vaaleanpunaiseksi,
        jos kortti on lukittu. Jos lukittua nappia painaa uudelleen, muuttuu
        se vaaleanvihreäksi ja korttia ei ole enää lukittu.
        :param numero: lukitse-napin numero
        """
        PlaySound("valitse.wav",1)
        self.__valitseArvot[numero-1] += 1
        if self.__valitseArvot[numero-1]%2 != 0:
            Button(self.__mainwindow,text="Lukittu",bg="pink"
                   ,command=lambda: self.lukitse(numero)) \
                .grid(row=4, column=numero,rowspan=3,padx=10,sticky=W+E)
        else:
            Button(self.__mainwindow,text="Lukitse",bg="lightgreen" ,
                   command=lambda: self.lukitse(numero)) \
                .grid(row=4, column=numero,rowspan=3,padx=10,sticky=W+E)


    def alusta_napit(self,numero):
        """
        Aktivoi lukitse-napit.
        :param numero: lukitse-napin numero
        """
        Button(self.__mainwindow,text="Lukitse",bg="lightgreen" ,
               command=lambda: self.lukitse(numero+1)) \
                .grid(row=4, column=numero+1,rowspan=3,padx=10,sticky=W+E)
        for i in range(5):
            self.__valitseArvot[i] = 0


    def alusta_korttipakka(self):
        """
        Alustaa korttipakan ja lisää siihen lisäjokereita,
        jos pelaaja on niitä ostanut.
        """
        self.__Korttipakka = []
        for i in range(54):
            self.__Korttipakka.append(i)
        for i in range(self.__extrajokerit):
            self.lisää_jokeri(self.__extrajokerit)

    def tarkista_voitto(self):
        """
        Tarkistaa pelaajan voiton. Päivittää pelimerkkien uuden määrän
        ja uuden panoksen näytölle.

        Kehitettävää: värisuoran, suoran ja täyskäden
                        tarkistuksessa saatta olla virheitä.
        :param pelikortit: pelaajan käsikortit
        :param kerroin: tietyn käden voittokerroin
        :param kaksiparia: laskee parien määrän
        :param nimi: voittokäden nimi
        :param maat: käsikorttien maat
        :param arvot: käsikorttien arvot
        :param tarkistus: käsikorttien arvot, mutta poistaa arvojen monikerrat
        """
        pelikortit = []
        kerroin = 0
        kaksiparia = 0
        nimi = ""
        maat = []
        arvot = []
        tarkistus = []
        for kortti in self.__pelikortit:
        #lisää kortin numeron listaan, aluksi kortti muotoa pyimage'numero'
        #[7:] jälkeen kortti muotoa 'numero'
            pelikortit.append(int(kortti["image"][7:]))
        for luku in pelikortit:
            maat.append(self.__tarkistus[luku][0])
            arvot.append(self.__tarkistus[luku][1])
        for luku in arvot:
            if luku not in tarkistus:
                tarkistus.append(luku)
        tarkistus = sorted(tarkistus)
        arvot = sorted(arvot)
        maat = sorted(maat)
        jokereiden_lkm = arvot.count(100)
        if arvot[4-jokereiden_lkm] == 13 and tarkistus[0] == 1 and tarkistus[1] > 9:
            ässä = 1
        else:
            ässä = 0

        if maat.count(maat[0]) == (5 - jokereiden_lkm):
            kerroin = 8
            nimi = "Väri"
        if len(tarkistus) == len(arvot) or jokereiden_lkm > 1:
            if arvot[4-jokereiden_lkm] - arvot[ässä]in range(0,5):
                if kerroin == 8:
                    kerroin = 150
                    nimi = "Värisuora"
                else:
                    kerroin = 5
                    nimi = "Suora"

        for arvo in tarkistus:
            if arvot.count(arvo) == 5:
                kerroin = 500
                nimi = "Viisi jokeria"

            if arvo == 100:
                continue
            if arvot.count(arvo) == 2:
                kaksiparia += 1
            if arvot.count(arvo) == (2-jokereiden_lkm) and \
                    (arvo > 10 or arvo == 1) and kerroin == 0:
                kerroin = 1
                nimi = "Jätkäpari tai parempi"
            if arvot.count(arvo) == (3-jokereiden_lkm) and kerroin < 3:
                kerroin = 3
                nimi = "Kolmoset"
            if kaksiparia in range(1,3) and kerroin ==3 and\
                            len(tarkistus) in range(2,4):
                kerroin = 15
                nimi = "Täyskäsi"
            if arvot.count(arvo) == (4-jokereiden_lkm) and kerroin < 25:
                kerroin = 25
                nimi = "Neloset"
            if arvot.count(arvo) == (5-jokereiden_lkm) and kerroin < 200:
                kerroin = 200
                nimi = "Vitoset"
            if kaksiparia == 2 and kerroin < 2:
                kerroin = 2
                nimi = "Kaksi paria"

        self.__mpelimerkit.set("Pelimerkit: {} + {}"
                .format(self.muuta_lukuasua(self.__pelimerkit),
                        self.muuta_lukuasua(self.__panos*kerroin)))
        if kerroin > 10:
            PlaySound('fanfare.wav',1)

        if kerroin >0 and kerroin < 10:
            PlaySound('voitto.wav',1)

        if kerroin == 0:
            if self.__pelimerkit != 0:
                PlaySound("häviö.wav",1)

            self.__teksti.set("Ei voittoa.")
        else:
            self.__teksti.set(nimi + ", voitit: {}"
                              .format(self.muuta_lukuasua(self.__panos*kerroin)))
        self.__mainwindow.update_idletasks()
        time.sleep(0.2)
        self.__pelimerkit += self.__panos * kerroin
        self.__mpelimerkit.set("Pelimerkit: {}"
                               .format(self.muuta_lukuasua(self.__pelimerkit)))
        if self.__panos < int(self.__pelimerkit*0.1+0.5) or self.__panosMAX >0:
            self.__panos = int(self.__pelimerkit*0.1+0.5)
        if self.__panos > self.__pelimerkit:
            self.__panos = self.__pelimerkit
        self.__panosMAX = 0
        self.__mpanos.set("Panos: {}".format(self.muuta_lukuasua(self.__panos)))

    def luo_tarkistus(self):
        """
        Luo listan, jossa jokaisella kortilla on arvo ja maa. Jokereille
        annettu arvoksi '100' ja maaksi 'ylläri', jotta ne ovat helposti
        järjesteltävissä muista korteista erilleen sorted-funktiolla.
        """
        laskuri = 0
        for i in range(len(self.__korttikuvat)):
            laskuri +=1
            if laskuri <14:
                if i%13 == 0:
                    self.__tarkistus[i] =["ruutu",13]
                else:
                    self.__tarkistus[i] =["ruutu",i%13]
            elif laskuri <27:
                if i%13 == 0:
                    self.__tarkistus[i] =["risti",13]
                else:
                    self.__tarkistus[i] =["risti",i%13]
            elif laskuri <41:
                if i%13 == 0:
                    self.__tarkistus[i] =["hertta",13]
                else:
                    self.__tarkistus[i] =["hertta",i%13]
            elif laskuri <=53:
                if i%13 == 0:
                    self.__tarkistus[i] =["pata",13]
                else:
                    self.__tarkistus[i] =["pata",i%13]
            elif laskuri > 53:
                self.__tarkistus[i] = ["ylläri",100]

    def lisää_jokeri(self,jokerit):
        """
        Lisää korttipakkaan ylimääräisiä jokereita. Joka toinen jokeri on musta
        ja joka toinen punainen.
        :param jokerit: lisäjokereiden lukumäärä
        """
        if jokerit == 0:
            return
        else:
            if jokerit%2 == 0:
                self.__Korttipakka.append(53)
            else:
                self.__Korttipakka.append(52)

    def osta_jokeri(self):
        """
        Lisää uuden jokerin pakkaan. Jos pelaajalla ei ole tarpeeksi pisteitä
        päivittää näytölle virhetekstin. Onnistuneesta ostosta päivittää
        pakkaan uuden jokerin ja näytölle tekstin ostosta.
        """
        if self.__tulos >= self.__jokerihinta:
            PlaySound('osto.wav',1)
            self.__extrajokerit += 1
            self.__jokeriteksti.set("Lisäjokereita: {}"
                                    .format(self.__extrajokerit))
            self.__teksti.set("Extrajokeri lisätty pakkaan!")
            self.__mtulos.set("Pisteet: {} - {}"
                            .format(self.muuta_lukuasua(self.__tulos),
                                self.muuta_lukuasua(self.__jokerihinta)))
            self.__mpelimerkit.set("Pelimerkit: {} /2"
                            .format(self.muuta_lukuasua(self.__pelimerkit)))
            self.__mpanos.set("Panos: {} /2"
                            .format(self.muuta_lukuasua(self.__panos)))
            self.__mainwindow.update_idletasks()
            time.sleep(1)
            self.__tulos -= self.__jokerihinta
            self.__mtulos.set("Pisteet: {}"
                            .format(self.muuta_lukuasua(self.__tulos)))
            self.__jokerihinta *= 5
            self.__panos = self.__panos/2
            self.__mpanos.set("Panos: {}"
                            .format(self.muuta_lukuasua(self.__panos)))
            self.__pelimerkit = self.__pelimerkit/2
            self.__mpelimerkit.set("Pelimerkit: {}"
                            .format(self.muuta_lukuasua(self.__pelimerkit)))
            self.__jokerihintaVar.set("Osta lisäjokeri: ({})"
                            .format(self.muuta_lukuasua(self.__jokerihinta)))
            self.alusta_korttipakka()
        else:
            PlaySound('error.wav',1)
            self.__teksti.set("Sinulla ei ole tarpeeksi pisteitä"
                              " ostaaksesi lisäjokeria")

    def muuta_lukuasua(self, arvo):
        """
        Muutta arvojen lukuasut SI-järjestelmän mukaisiin kertoimiin.
        :param arvo: muutettava arvo
        """
        arvo = int(arvo)
        k = 1000
        M = 1000*k
        G = 1000*M
        T = 1000*G

        if arvo >= T:
            arvo = str(int(arvo/T)) + "T"
            return arvo
        if arvo >= G and arvo < 1000*G:
            arvo = str(int(arvo/G)) + "G"
            return arvo
        if arvo >= M and arvo < G:
            arvo = str(int(arvo/M)) + "M"
            return arvo
        if arvo >= 10*k and arvo < M:
            arvo = str(int(arvo/k)) + "k"
            return arvo
        if arvo <= 10*k:
            return arvo



def main():
    GUI()



main()

