import tkinter as tk
import numpy as np
from datetime import datetime
import sys
from cryptography.fernet import Fernet
import os
from github import Github
from PIL import Image,ImageTk
import requests
from io import BytesIO
import re
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
        if tt == 3:
            repository_name = 'PStarUnicron/JuL'
            file_path = 'M3.txt'
            MA = read_github_file(repository_name,file_path,branch)
        MA = MA.encode('utf-8')
        cipher_suite = Fernet(rr)
        MA = eval(cipher_suite.decrypt(MA).decode())
        return MA

    def open_navigation_window(fenetre,selected_value, tot, num_question, nb_pts_tot,nb_used,uncorr):
        fenetre.config(bg='grey')
        def photo(fenetre,name):
            def import_image_from_github(repository_name, image_path, branch='master', token=None):
                if token:
                    headers = {'Authorization': f'token {token}'}
                else:
                    headers = {}

                github_raw_url = f'https://raw.githubusercontent.com/{repository_name}/{branch}/{image_path}'

                try:
                    response = requests.get(github_raw_url, headers=headers)
                    response.raise_for_status()

                    # Get the image content as bytes
                    image_content = BytesIO(response.content)

                    # Open and display the image using PIL
                    image = Image.open(image_content)
                    return image

                except Exception as e:
                    print(f"Error: {e}")
            frame = tk.Frame(fenetre)
            frame.pack()

            #status bar
            bar = tk.Frame(fenetre, relief='ridge', borderwidth=5)
            bar.pack(side='top')
            repository_name = 'PStarUnicron/JuL'
            image_path = f'IMG/{name}'
            branch = 'main'

            iconPath = import_image_from_github(repository_name, image_path, branch)
            icon = ImageTk.PhotoImage(iconPath)
            icon_size = tk.Label(bar)
            icon_size.image = icon
            icon_size.configure(image=icon)
            icon_size.pack(side='left')

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
        def get_github_directory_files(repo_owner, repo_name, directory_path, token=None):
            base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{directory_path}'
            headers = {'Accept': 'application/vnd.github.v3+json'}

            if token:
                headers['Authorization'] = f'token {token}'

            files = []

            try:
                response = requests.get(base_url, headers=headers)
                response.raise_for_status()

                contents = response.json()

                for item in contents:
                    if 'type' in item and item['type'] == 'file':
                        files.append(item['name'])

                return files
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération des fichiers : {e}")
                return []
        def del_butt():
            correction_button.destroy()
        clear_window(fenetre)
        variables = [tk.IntVar() for _ in range(4)]
        label1 = tk.Label(fenetre, text=f"{selected_value[0]}",wraplength=800,bg='grey')
        label1.pack(pady=5)
        label_line_break1 = tk.Label(fenetre, text="",bg='grey')
        label_line_break1.pack(pady=5)
        repository_owner = 'PStarUnicron'
        repository_name = 'JuL'
        directory_path = 'IMG'  
        github_token = ''  
        files_list = get_github_directory_files(repository_owner, repository_name, directory_path, github_token)
        match = re.search(r'(\d+)\.', selected_value[0])
        if match:
            chiffre_avant_point = int(match.group(1))
            chiffre_avant_point = str(chiffre_avant_point)+'.JPG'
            if chiffre_avant_point in files_list:
                photo(fenetre,chiffre_avant_point)
        label2 = tk.Label(fenetre, text="Réponses :",bg='grey')
        label2.pack(pady=5)
        label_line_break2 = tk.Label(fenetre, text="",bg='grey')
        label_line_break2.pack(pady=5)

        buttons = [tk.Checkbutton(fenetre, text=f"[{i+1}] {selected_value[1][i]}", variable=var,wraplength=800,bg='grey') for i, var in enumerate(variables)]

        for button in buttons:
            button.pack()
        correction_button = tk.Button(fenetre, text="Correction", command=lambda: (update_button_colors(buttons,selected_value[2]),del_butt(),show_correction(fenetre,selected_value[2], tot,variables,num_question,nb_pts_tot,nb_used,uncorr)),bg='lightgrey')
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

    def show_correction(fenetre,correction_value, tot,variables,num_question,nb_pts_tot,nb_used,uncorr):
        def afficher_score(nb_pts,num_question,nb_used,tot):
            def change_state(evo):
                if evo == 1:
                    state[0]=1
                else:
                   state[0]=0 
            def assigner_valeur(base,valeur,memory,add):
                variable_globale.set(base+valeur)
                afficher_resultat(memory,add)
            def recorr (tot,uncorr):
                open_navigation_window(fenetre,tot[uncorr[num_uncorr[0]]], tot,num_question,nb_pts_tot,nb_used,uncorr)
            def more_question(num_question,nb_used,tot,uncorr):
                prevention = tk.Label(fenetre,text='Attention, chaque appuie ajoutera le nombre de questions',wraplength=700,bg='grey')
                prevention.pack(pady=10)
                valeurs_boutons = [5,10]
                memory = variable_globale.get()
                for valeur in valeurs_boutons:
                    bouton = tk.Button(fenetre, text=str(valeur)+' questions', command=lambda v=valeur: assigner_valeur(variable_globale.get(),v,memory,add),bg='lightgrey')
                    bouton.pack(side=tk.TOP, padx=5)
                add = tk.Label(fenetre,text='',bg='grey')
                add.pack(pady=10)
                num_question += 1
                selected_value,nb_used = pick_num(nb_used,tot)
                letsgo = tk.Button(fenetre,text='LETSGO',command=lambda:open_navigation_window(fenetre,selected_value, tot,num_question,nb_pts_tot,nb_used,uncorr),bg='lightgrey')
                letsgo.pack(pady=10)
            def reload():
                python = sys.executable
                os.execl(python, python, *sys.argv)
            def afficher_resultat(memory,add): 
                nq = variable_globale.get()-memory
                add.config(text=f"Il y a actuellement {nq} questions en plus ({variable_globale.get()} au total)")
            score_final = tk.Label(fenetre,text=f"Vous avez obenu un score de {round(nb_pts,2)} sur {variable_globale.get()}",bg='purple')
            score_final.pack(pady=10)
            reload_butt = tk.Button(fenetre,text='Relancer programme',command=lambda:reload(),bg='purple')
            reload_butt.pack(pady=10)
            more_qq = tk.Button(fenetre,text='JE VEUX PLUS DE QUESTIOOOOOONS',command=lambda:more_question(num_question,nb_used,tot,uncorr),bg='red')
            more_qq.pack(pady=10)
            if uncorr != []:
                retry = tk.Button(fenetre,text='Refaire les questions auxquelles j ai échoué',command=lambda:(recorr(tot,uncorr),change_state(1)))
                retry.pack(pady=10)
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
        if state[0] == 0:
            nb_pts_tot += nb_pts
        if nb_pts!= 1 and state[0] == 0:
            uncorr += [nb_used[num_question-1]]
        nb_correctes_label = tk.Label(fenetre,text="",bg='grey')
        nb_correctes_label.pack()  
        if len(boutons_coches)>nb_correctes:
            nb_correctes_label.config(text = f"Soit {nb_correctes} bonnes réponse sur {len(nouveaux_chiffres)} ({round(nb_pts,2)} points car {len(boutons_coches)-nb_correctes} réponse fausse)",bg='grey',wraplength=700)
        else:
            nb_correctes_label.config(text = f"Soit {nb_correctes} bonnes réponse sur {len(nouveaux_chiffres)} ({round(nb_pts,2)} points)",bg='grey',wraplength=700)
        if state[0] == 1:
            num_uncorr[0] = num_uncorr[0]+1
            print(f'going into {num_uncorr[0]} question')
            print(uncorr)
            if num_uncorr[0] == len(uncorr):
                num_uncorr[0] = 0
                uncorr = []
                state[0] = 0
                afficher_score(nb_pts_tot,num_question,nb_used,tot)
            else:
                go_on_button = tk.Button(fenetre, text="Next question", command=lambda:(open_navigation_window(fenetre,tot[uncorr[num_uncorr[0]]], tot,num_question,nb_pts_tot,nb_used,uncorr)),bg='lightgrey')
                go_on_button.pack(pady=10)    
        else:
            if num_question >= variable_globale.get():
                afficher_score(nb_pts_tot,num_question,nb_used,tot)
            else:
                score_actuel = tk.Label(fenetre,text=f"Vous avez actuellement {round(nb_pts_tot,2)} sur {num_question}",bg='purple')
                score_actuel.pack()  
                num_question += 1
                selected_value,nb_used = pick_num(nb_used,tot)
                go_on_button = tk.Button(fenetre, text="Next question", command=lambda:(open_navigation_window(fenetre,selected_value, tot,num_question,nb_pts_tot,nb_used,uncorr)),bg='lightgrey')
                go_on_button.pack(pady=10) 
                fenetre.wait_window()

    def on_m1_click(fenetre):
        tot = Get_bdd(1,b'UBZuKooAiOrK7uZFvXhwZXAF8l0ZAz8Rk6lhwOg_SDU=')
        selected_value, nb_used = pick_num([],tot)
        open_navigation_window(fenetre,selected_value, tot,1,0,nb_used,[])
    def on_m2_click(fenetre):
        tot = Get_bdd(2,b'hJQlp7NFy--5DmSW-8KuG6k6coOTmtdic_tNb1_nILc=')
        selected_value, nb_used = pick_num([],tot)
        open_navigation_window(fenetre,selected_value, tot,1,0,nb_used,[])
    def on_m3_click(fenetre):
        tot = Get_bdd(3,b'UBZuKooAiOrK7uZFvXhwZXAF8l0ZAz8Rk6lhwOg_SDU=')
        selected_value, nb_used = pick_num([],tot)
        open_navigation_window(fenetre,selected_value, tot,1,0,nb_used,[])
    def fermer_programme():
        sys.exit()
    def afficher_resultat():
        resultat_label.config(text=f"Il y a actuellement {variable_globale.get()} questions")
    def assigner_valeur(valeur):
        variable_globale.set(valeur)
        afficher_resultat()
    def import_image_from_github(repository_name, image_path, branch='master', token=None):
        if token:
            headers = {'Authorization': f'token {token}'}
        else:
            headers = {}

        github_raw_url = f'https://raw.githubusercontent.com/{repository_name}/{branch}/{image_path}'

        try:
            response = requests.get(github_raw_url, headers=headers)
            response.raise_for_status()

            # Get the image content as bytes
            image_content = BytesIO(response.content)

            # Open and display the image using PIL
            image = Image.open(image_content)
            return image

        except Exception as e:
            print(f"Error: {e}")
    ############################################################################################################################################
    td = datetime.now().date()

    dd = datetime(2024, 4,1).date()

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
    repository_name = 'PStarUnicron/JuL'
    image_path = 'IMG/welding-181656_640.jpg'
    branch = 'main'

    image = import_image_from_github(repository_name, image_path, branch)

    img = image
    img = img.resize((fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()), Image.BICUBIC)
    background_image = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(fenetre, width=fenetre.winfo_screenwidth(), height=fenetre.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=background_image)

    variable_globale = tk.IntVar()

    valeurs_boutons = [5,10, 15, 20, 46]
    t =0
    for valeur in valeurs_boutons:
        bouton = tk.Button(fenetre, text=str(valeur)+' questions', command=lambda v=valeur: assigner_valeur(v),bg='lightgrey')
        bouton.place(relx=0.5,rely=0.1+0.1*t,anchor='center')
        t+=1


    resultat_label = tk.Label(fenetre, text="",wraplength=1000)

    resultat_label.place(rely=0.55,relx=0.5,anchor='center')


    bouton_m1 = tk.Button(fenetre, text="M1", command=lambda:on_m1_click(fenetre),bg='lightgrey')
    bouton_m2 = tk.Button(fenetre, text="M2", command=lambda:on_m2_click(fenetre),bg='lightgrey')
    bouton_m3 = tk.Button(fenetre, text="M3", command=lambda:on_m3_click(fenetre),bg='lightgrey')
    bouton_m1.place(relx=0.5,rely=0.6,anchor='center')
    bouton_m2.place(relx=0.5,rely=0.7,anchor='center')
    bouton_m3.place(relx=0.5,rely=0.8,anchor='center')
    version = tk.Label(fenetre,text='Version mise à jour le 29/02/2024', wraplength=700)
    version.place(relx=0.5,rely=0.9,anchor='center')
    state = [0]
    num_uncorr = [0]
    fenetre.mainloop()
