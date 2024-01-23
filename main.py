import tkinter as tk
import numpy as np
from datetime import datetime
import sys
from cryptography.fernet import Fernet
import os
from github import Github
# -*- coding: utf-8 -*-
def train():
    def Get_bdd (tt,rr):
        def read_github_file(repository_name, file_path, branch='master', token=None):
            if token:
                g = Github(token)
            else:
                g = Github()

            try:
                repo = g.get_repo(repository_name)
                contents = repo.get_contents(file_path, ref=branch)
                file_content = contents.decoded_content.decode('utf-8')
                return file_content
            except Exception as e:
                return f"Error: {e}"

        repository_name = 'PStarUnicron/JuL'
        branch = 'main'
        if tt == 1:
            file_path = 'M1.txt'
            MA = read_github_file(repository_name,file_path,branch)
        if tt == 2:
            repository_name = 'PStarUnicron/JuL'
            file_path = 'M2.txt'
            MA = read_github_file(repository_name,file_path,branch)
        MA = MA.encode('utf-8')
        cipher_suite = Fernet(rr)
        MA = eval(cipher_suite.decrypt(MA).decode())
        return MA

    def open_navigation_window(fenetre,selected_value, tot, num_question, nb_pts_tot,nb_used):
        def clear_window(window):

            widgets = window.winfo_children()

            for widget in widgets:
                widget.destroy()
        def update_button_colors(buttons,correction_value):
            nouveaux_chiffres = [str(int(chiffre.strip()) + 1) for chiffre in correction_value.split(",") if chiffre.strip()]
            for i, button in enumerate(buttons):
                if str(i+1) in nouveaux_chiffres:
                    button.config(bg='green')
                else:
                    button.config(bg='red')

        def del_butt():
            correction_button.destroy()
        clear_window(fenetre)
        # navigation_window = tk.Toplevel(fenetre)
        # navigation_window.title("Révision")
        # navigation_window.configure(bg='grey')
        variables = [tk.IntVar() for _ in range(4)]
        label1 = tk.Label(fenetre, text=f"{selected_value[0]}",wraplength=800,bg='grey')
        label1.pack(pady=5)
        label_line_break1 = tk.Label(fenetre, text="",bg='grey')
        label_line_break1.pack(pady=5)
        label2 = tk.Label(fenetre, text="Réponses :",bg='grey')
        label2.pack(pady=5)
        label_line_break2 = tk.Label(fenetre, text="",bg='grey')
        label_line_break2.pack(pady=5)

        # Créer les Checkbuttons et stocker les références dans une liste
        buttons = [tk.Checkbutton(fenetre, text=f"[{i+1}] {selected_value[1][i]}", variable=var,wraplength=800,bg='grey') for i, var in enumerate(variables)]

        for button in buttons:
            button.pack()
        correction_button = tk.Button(fenetre, text="Correction", command=lambda: (update_button_colors(buttons,selected_value[2]),del_butt(),show_correction(fenetre,selected_value[2], tot,variables,num_question,nb_pts_tot,nb_used)),bg='lightgrey')
        correction_button.pack(pady=10)
        nq = tk.Label(fenetre, text=f"Question n°{num_question} sur {variable_globale.get()}",bg='grey')
        nq.pack(pady=10)
    def pick_num (nb_used,tot):
        random_index = np.random.randint(len(tot))
        while random_index in nb_used:
            random_index = np.random.randint(len(tot))
        selected_value = tot[random_index]
        nb_used += [random_index]
        return selected_value,nb_used
    def destroyer (window):
        window.destroy()

    def show_correction(fenetre,correction_value, tot,variables,num_question,nb_pts_tot,nb_used):
        def afficher_score(nb_pts,num_question,nb_used,tot):
            def afficher_resultat(memory,add):
													nq = variable_globale.get()-memory 
                add.config(text=f"Il y a actuellement {nq} questions en plus ({variable_globale.get()} au total)")
            def assigner_valeur(base,valeur,memory,add):
                variable_globale.set(base+valeur)
                afficher_resultat(memory,add)
            def more_question(num_question,nb_used,tot):
                add = tk.Label(fenetre,text='',bg='grey')
                add.pack(pady=10)
                prevention = tk.Label(fenetre,text='Attention, chaque appuie ajoutera le nombre de questions',wraplength=700,bg='grey')
                prevention.pack(pady=10)
                valeurs_boutons = [5,10]
                memory = variable_globale.get()
                for valeur in valeurs_boutons:
                    bouton = tk.Button(fenetre, text=str(valeur)+' questions', command=lambda v=valeur: assigner_valeur(variable_globale.get(),v,memory,add),bg='lightgrey')
                    bouton.pack(side=tk.TOP, padx=5)
                num_question += 1
                selected_value,nb_used = pick_num(nb_used,tot)
                letsgo = tk.Button(fenetre,text='LETSGO',command=lambda:open_navigation_window(fenetre,selected_value, tot,num_question,nb_pts_tot,nb_used),bg='lightgrey')
                letsgo.pack(pady=10)
            def reload():
                python = sys.executable
                os.execl(python, python, *sys.argv)
            score_final = tk.Label(fenetre,text=f"Vous avez obenu un score de {round(nb_pts,2)} sur {variable_globale.get()}",bg='purple')
            score_final.pack(pady=10)
            reload_butt = tk.Button(fenetre,text='Relancer programme',command=lambda:reload(),bg='purple')
            reload_butt.pack(pady=10)
            more_qq = tk.Button(fenetre,text='JE VEUX PLUS DE QUESTIOOOOOONS',command=lambda:more_question(num_question,nb_used,tot),bg='red')
            more_qq.pack(pady=10)
        resultat_label = tk.Label(fenetre, text="",bg='grey')
        resultat_label.pack()
        boutons_coches = []
        for i, var in enumerate(variables):
            if var.get() == 1:
                boutons_coches.append(i + 1)
        
        resultat_label.config(text=f"Réponses cochés : {boutons_coches}")
        correct_label = tk.Label(fenetre, text="",bg='grey')
        correct_label.pack()
        nouveaux_chiffres = [str(int(chiffre.strip()) + 1) for chiffre in correction_value.split(",") if chiffre.strip()]
        Num_corr = ", ".join(nouveaux_chiffres)
        nouveaux_chiffres = [int(element) for element in nouveaux_chiffres]
        correct_label.config(text=f"Réponses correctes : {Num_corr}")
        nb_correctes = sum(1 for proposition in boutons_coches if proposition in nouveaux_chiffres)
        nb_pts = nb_correctes
        if len(boutons_coches)>nb_correctes:
            nb_pts = nb_pts - (len(boutons_coches)-nb_correctes)
            if nb_pts < 0:
                nb_pts = 0
        nb_pts = nb_pts/len(nouveaux_chiffres)
        nb_pts_tot += nb_pts
        nb_correctes_label = tk.Label(fenetre,text="",bg='grey')
        nb_correctes_label.pack()  
        if len(boutons_coches)>nb_correctes:
            nb_correctes_label.config(text = f"Soit {nb_correctes} bonnes réponse sur {len(nouveaux_chiffres)} ({round(nb_pts,2)} points car {len(boutons_coches)-nb_correctes} réponse fausse)",bg='grey',wraplength=700)
        else:
            nb_correctes_label.config(text = f"Soit {nb_correctes} bonnes réponse sur {len(nouveaux_chiffres)} ({round(nb_pts,2)} points)",bg='grey',wraplength=700)
        
        if num_question >= variable_globale.get():
            afficher_score(nb_pts_tot,num_question,nb_used,tot)
        else:
            score_actuel = tk.Label(fenetre,text=f"Vous avez actuellement {round(nb_pts_tot,2)} sur {num_question}",bg='purple')
            score_actuel.pack()  
            num_question += 1
            selected_value,nb_used = pick_num(nb_used,tot)
            go_on_button = tk.Button(fenetre, text="Next question", command=lambda:(open_navigation_window(fenetre,selected_value, tot,num_question,nb_pts_tot,nb_used)),bg='lightgrey')
            go_on_button.pack(pady=10) 
            fenetre.wait_window()

    def on_m1_click(fenetre):
        tot = Get_bdd(1,b'UBZuKooAiOrK7uZFvXhwZXAF8l0ZAz8Rk6lhwOg_SDU=')
        selected_value, nb_used = pick_num([],tot)
        open_navigation_window(fenetre,selected_value, tot,1,0,nb_used)
    def on_m2_click(fenetre):
        tot = Get_bdd(2,b'hJQlp7NFy--5DmSW-8KuG6k6coOTmtdic_tNb1_nILc=')
        selected_value, nb_used = pick_num([],tot)
        open_navigation_window(fenetre,selected_value, tot,1,0,nb_used)
    def fermer_programme():
        sys.exit()
    def afficher_resultat():
        resultat_label.config(text=f"Il y a actuellement {variable_globale.get()} questions")
    def assigner_valeur(valeur):
        variable_globale.set(valeur)
        afficher_resultat()


    ############################################################################################################################################
    td = datetime.now().date()

    dd = datetime(2024, 2,1).date()

    if td > dd:
        fenetre = tk.Tk()
        fenetre.title("Message d'expiration")

        label_message = tk.Label(fenetre, text="Période de validité terminée")
        label_message.pack(padx=20, pady=20)

        bouton_ok = tk.Button(fenetre, text="OK", command=fermer_programme)
        bouton_ok.pack(pady=10)

        fenetre.mainloop()
    ############################################################################################################################################
    fenetre = tk.Tk()
    fenetre.title("Choix du module")
    fenetre.configure(bg='grey')

    variable_globale = tk.IntVar()

    valeurs_boutons = [5, 15, 20, 35, 46]
    for valeur in valeurs_boutons:
        bouton = tk.Button(fenetre, text=str(valeur)+' questions', command=lambda v=valeur: assigner_valeur(v),bg='lightgrey')
        bouton.pack(side=tk.TOP, padx=5)

    resultat_label = tk.Label(fenetre, text="",wraplength=1000,bg='grey')
    resultat_label.pack(pady=10)


    bouton_m1 = tk.Button(fenetre, text="M1", command=lambda:on_m1_click(fenetre),bg='lightgrey')
    bouton_m2 = tk.Button(fenetre, text="M2", command=lambda:on_m2_click(fenetre),bg='lightgrey')
    bouton_m1.pack(side = tk.TOP ,padx = 5)
    bouton_m2.pack(side = tk.TOP, padx = 5)

    fenetre.mainloop()
