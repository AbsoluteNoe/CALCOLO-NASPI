from datetime import datetime
import calendar

def calcola_scadenza_naspi():
    # 1. Acquisizione degli input dall'utente
    data_input = input("Inserisci la data di inizio (Formato GG/MM/AAAA): ")
    try:
        giorni_rimanenti = int(input("Inserisci i giorni di erogazione: "))
    except ValueError:
        print("Errore: I giorni di erogazione devono essere un numero intero.")
        return

    try:
        data_corrente = datetime.strptime(data_input, "%d/%m/%Y")
    except ValueError:
        print("Errore: Formato data non valido. Usa il formato GG/MM/AAAA.")
        return

    anno = data_corrente.year
    mese = data_corrente.month
    giorno = data_corrente.day
    
    # Variabile di controllo per identificare il primo mese
    primo_mese = True

    # Funzione interna per determinare la durata del mese secondo le regole
    def giorni_massimi_mese(m, a, is_first):
        # Il primo mese in assoluto usa i giorni effettivi del calendario reale
        if is_first:
            _, giorni_reali = calendar.monthrange(a, m)
            return giorni_reali
        
        # Dal secondo mese in poi si applica la regola commerciale
        if m == 2:
            is_bisestile = (a % 4 == 0 and a % 100 != 0) or (a % 400 == 0)
            return 29 if is_bisestile else 28
        return 30

    # 2. Sviluppo del calendario per consumare i giorni di NASpI
    while giorni_rimanenti > 0:
        max_giorni = giorni_massimi_mese(mese, anno, primo_mese)
        giorni_disponibili_nel_mese = max_giorni - giorno + 1

        # Se i giorni che mancano alla fine del mese coprono o superano la NASpI rimasta
        if giorni_rimanenti <= giorni_disponibili_nel_mese:
            giorno_fine = giorno + giorni_rimanenti - 1
            
            # Riconversione estetica finale se siamo oltre il primo mese: 
            # se il giorno calcolato è il 30° di un mese commerciale che nella realtà ne ha 31, mostriamo il 31
            if not primo_mese:
                _, giorni_reali_calendario = calendar.monthrange(anno, mese)
                if giorni_reali_calendario == 31 and giorno_fine == 30:
                    giorno_fine = 31
                
            print(f"La tua naspi cesserà il: {giorno_fine:02d}/{mese:02d}/{anno}")
            break
        else:
            # Consumiamo i giorni disponibili in questo mese e passiamo al successivo
            giorni_rimanenti -= giorni_disponibili_nel_mese
            mese += 1
            if mese > 12:
                mese = 1
                anno += 1
            giorno = 1
            # Dal prossimo ciclo in poi non siamo più nel primo mese
            primo_mese = False

# Esecuzione del programma
if __name__ == "__main__":
    calcola_scadenza_naspi()
