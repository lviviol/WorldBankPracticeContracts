# WorldBank Contract Awards  

**Purpose**  
1. Analysis World Bank Contract Awards in Investment Projects Financing for various regions.

**How**  
1. Differentiate region's yearly awards quantum by size of bubble.
2. Bubble size is the US$(mil) value of the awarded contract for each region in respective years.
3. Identify practices and relative frequency where the awards are being funded by World Bank.
4. SQLite & Python are used for compiling this data due SQL's efficient interation with database and Python's versatility and flexibility.
   

**Challenges**  
1. Total Value of Practices are combined, and thus is not possible to distinguish nor derive actual award amount for each practice.
2. For example, "Europe and Central Asia" was awared fundings for "Health; Agriculture, Fishing and Forestry".  Therefore, it is not possible to differentiate funding quantum between "Health" & "Agriculture, Fishing and Forestry"

**How to Resolve Challenge?**  
1. Count/frequency of each practice is used to identify and understand how often each region is being awarded.

.  
.  

**Analysis A: Bubble Plot of Total Value vs Regions**  
1. Emerging markets, namely African regions and South Asia are receiving stable or growing Contract Awards from World Bank's Investment Project Financing program.
2. Rest of the world, mainly developed continents are receiving less.
3. Middle East, North Africa, Latin America and Caribbean receives least award.  It is unclear if application quantum is lower.

![alt text](https://github.com/lviviol/WorldBankPracticeContracts/blob/main/WBProjects.png?raw=true)  
.  
.  

**Analysis B: Stacked Bar on Frequency/Count of Practices**  
1. African and South Asian regions are seeking more investments in infrastructures such as Transportation and Public Administration.  On humanitarian perspective, Social Protection has equally high counts of contracts awarded.
3. Middle East & Latin Amerian are highly participative in Agriculture, Fishing and Forestry. 
4. Asia is actively seeking Industrialization and Trade services.
5. Europe & Central Asia, relatively more developed regions, seems more focused on Water, Sanitation and Waste Management.

![alt text](https://github.com/lviviol/WorldBankPracticeContracts/blob/main/WBPractice.png?raw=true)  
