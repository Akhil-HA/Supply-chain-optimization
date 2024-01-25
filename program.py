


import tkinter as tk
import numpy as np
import pandas as pd
import math

class FormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joint Replenishment Analysis Tool")
        

        self.num_entries_var = tk.IntVar()
        self.HC = tk.IntVar()
        self.FC = tk.IntVar()
        
        
        self.page_index = 0  # To keep track of the current page

        self.create_first_page()

    def create_first_page(self):
        first_page = tk.Frame(self.root)
        first_page.pack()

        label = tk.Label(first_page, text="Enter the number of SKUs:")
        label.pack(pady=10)

        entry = tk.Entry(first_page, textvariable=self.num_entries_var)
        entry.pack(pady=10)

        submit_button = tk.Button(first_page, text="Submit", command=self.show_form_page)
        submit_button.pack(pady=10)

    def show_form_page(self):
        try:
            num_entries = self.num_entries_var.get()
            if num_entries <= 0:
                raise ValueError("Number of entries must be greater than zero.")

            # Destroy the current page
            self.root.winfo_children()[self.page_index].destroy()

            form_page = tk.Frame(self.root)
            form_page.pack()
            

            entries = []
            for i in range(num_entries):
                label_demand = tk.Label(form_page, text=f"Demand for SKU {i + 1}:")
                label_demand.grid(row=3, column=i+2, padx=10, pady=5, sticky=tk.W)

                entry_demand = tk.Entry(form_page)
                entry_demand.grid(row=4, column=i+2, padx=10, pady=5, sticky=tk.W)

                entries.append(entry_demand)
                
                label_OC = tk.Label(form_page, text=f"Ordering cost for SKU {i + 1}:")
                label_OC.grid(row=6, column=i+2, padx=10, pady=5, sticky=tk.W)

                entry_OC = tk.Entry(form_page)
                entry_OC.grid(row=7, column=i+2, padx=10, pady=5, sticky=tk.W)
                entries.append(entry_OC)
                
                label_Price = tk.Label(form_page, text=f"Price for SKU {i + 1}:")
                label_Price.grid(row=9, column=i+2, padx=10, pady=5, sticky=tk.W)

                entry_Price = tk.Entry(form_page)
                entry_Price.grid(row=10, column=i+2, padx=10, pady=5, sticky=tk.W)
                entries.append(entry_Price)
                
                
                
                
                
                
            
            #for index, row in dF1.iterrows():print(row)
            #print(dF1.values)
            label_HC = tk.Label(form_page, text=f"Holding cost % :")
            label_HC.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

            entry_HC = tk.Entry(form_page, textvariable=self.HC)
            entry_HC.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
            
            
            label_FC = tk.Label(form_page, text=f"Fixed cost :")
            label_FC.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

            entry_FC = tk.Entry(form_page, textvariable=self.FC)
            entry_FC.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)
            
            
            result_text = tk.Text(form_page, height=7, width=60)
            result_text.grid(row=13, column=1, columnspan=5, pady=20, padx=10)
            

            submit_button = tk.Button(form_page, text="Submit", command=lambda: self.get_form_data(entries,result_text))
            submit_button.grid(row=11, column=1, columnspan=2, pady=10)

            self.page_index += 1  # Increment the page index
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def get_form_data(self, entries, result_text):
        n = self.num_entries_var.get()
        data = [entry.get() for entry in entries]
        new = pd.DataFrame()
        new['values'] = data
        #series_result = pd.DataFrame{["values": data]}
        #num_columns = len(new) // 3
        reshaped_values = [new['values'].iloc[i:i + 3].tolist() for i in range(0, len(new), 3)]
        #newcolumns = [f'Column{i+1}' for i in range(reshaped_values.shape[1])]
        dF1 = pd.DataFrame(reshaped_values)
        S = self.FC.get()
        HC = (self.HC.get())/100
        dF1 = dF1.apply(pd.to_numeric)
        dF1[3] = dF1[2].mul(HC).tolist()
        dF1 =dF1.T
        
        def individual_ordering():
            sum = 0
            for i in range (n):
                Qi = math.sqrt(2*dF1.iloc[0,i-1]*(dF1.iloc[1,i-1]+S)/dF1.iloc[3,i-1])
                Ni = dF1.iloc[0,i-1]/Qi
                Oc = Ni*(S+dF1.iloc[1,i-1])
                Icc = (dF1.iloc[3,i-1])*Qi/2
                sum = sum +Oc+ Icc
            return sum
        
        def complete_aggregation():
            sum = 0
            sum1 = 0
            for i in range(n):
                sum = sum + (dF1.iloc[0,i-1]*dF1.iloc[3,i-1])
                rowsum = (dF1.iloc[1:2].sum(axis = 1)).iloc[0]
            N =math.sqrt((sum)/(2*(S+rowsum)))
            for i in range(n):
                Icc = ((dF1.iloc[0,i-1]/N)/2)*dF1.iloc[3,i-1]
                sum1 = sum1+Icc
            return sum1 + (N*(rowsum+S))
        def Tailored_replenishment():
            Nlist = []
            Nilist =[]
            for i in range(n):
                Q = math.sqrt((2*dF1.iloc[0,i-1]*(dF1.iloc[1,i-1] + S))/dF1.iloc[3,i-1])
                N = dF1.iloc[0,i-1]/Q
                Nlist.append(N)
                Ni = math.sqrt((dF1.iloc[3,i-1]*dF1.iloc[0,i-1])/2/dF1.iloc[1,i-1])
                Nilist.insert(-1,Ni)
            Nmax = max(Nlist)
            multi = np.divide(Nmax,Nilist)
            ceil = pd.DataFrame(map(math.ceil,multi)).T
            denomi = pd.DataFrame(dF1.loc[1:1])
            den = 2*(S+((denomi.div(ceil.values)).sum(axis = 1)))
            num= (dF1.loc[0].mul(dF1.loc[3]).sum())
            N_prime = math.sqrt(num/den)
            ICC = 0
            avgc = 0
            for i in range(n):
                Q = ((dF1.iloc[0,i-1]/(N_prime/ceil.iloc[0,i-1]))/2)*(dF1.iloc[3,i-1])
                ICC+=Q
                avgc += dF1.iloc[1,i-1]*N_prime/ceil.iloc[0,i-1]
            return ICC + (N_prime*((avgc+(N_prime*S))/N_prime))
        IO =round(individual_ordering())
        CA= round(complete_aggregation())
        TR =round(Tailored_replenishment())


        # Display the Series in the text box
        result_text.delete(1.0, tk.END)  # Clear previous content
        result_text.insert(tk.END, f"Individual ordering:  {IO}\nComplete aggregation:  {CA}\nTailored replenishment:  {TR}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormApp(root)
    root.mainloop()