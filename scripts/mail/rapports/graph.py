import matplotlib.pyplot as plt

labels = 'Refusé', 'Discussion', 'Accepté'
sizes = [26, 4, 0]
labels = [labels[i] + ' (' + str(sizes[i]) + ')' for i in range(len(labels))]
colors = ['red', 'yellow', 'green']
explode = (0.1, 0.1, 0.1)

plt.pie(sizes, explode, labels, colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.savefig('result.png')
plt.clf()

answered = sum(sizes)
labels = 'Délivé', 'Erreur', 'Non délivré', 'Addresse changée'
sizes = [812, 611, 105]
sizes.insert(0, 32012 - sum(sizes))
labels = [labels[i] + ' (' + str(sizes[i]) + ')' for i in range(len(labels))]
colors = ['green', 'red', 'orange', 'yellow']
explode = (0.1, 0, 0.1, 0.2)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.savefig('send.png')
plt.clf()

labels = 'Non répondu', 'Répondu'
sizes = [sizes[0]-answered, answered]
labels = [labels[i] + ' (' + str(sizes[i]) + ')' for i in range(len(labels))]
colors = ['red', 'green']
explode = (0.1, 0)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        pctdistance=0.5, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.savefig('answers.png')
plt.clf()

