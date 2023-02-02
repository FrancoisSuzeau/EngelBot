import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from wordcloud import WordCloud, STOPWORDS

class Analysis():
    def __init__(self) -> None:
        pass
    
    def cluster_datas(self):
        df_read = pd.read_csv("materials/data/backup.csv", header=None, delimiter=';')
        df_read[0] = df_read[0].astype('string')
        for i in range(len(df_read[0])):
            df_read[0][i] = df_read[0][i] + ' '
        
        self.text = ''.join(df_read[0])
        sentences = df_read[0].to_numpy()
        # Create a dataframe from the list of sentences
        self.df = pd.DataFrame(sentences, columns=['sentence'])
        # Create an instance of the CountVectorizer class
        vectorizer = CountVectorizer()
        # Use the fit_transform method to create a bag-of-words representation of the sentences
        self.sentence_vectors = vectorizer.fit_transform(self.df['sentence']).toarray()
        # Create an instance of the KMeans class with the number of clusters you want
        kmeans = KMeans(n_clusters=5)
        # Use the fit_predict method to cluster the sentences
        self.clusters = kmeans.fit_predict(self.sentence_vectors)
        # Add the cluster labels to the dataframe
        self.df['cluster'] = self.clusters


    # calculate distortions for a range of number of cluster
    def elbow_with_distortions(self):
        distortions = []
        for i in range(1, 11):
            km = KMeans(
                n_clusters=i, init='random',
                n_init=10, max_iter=300,
                tol=1e-04, random_state=0
            )
            km.fit(self.sentence_vectors)
            distortions.append(km.inertia_)
        return distortions

    # calculate silhouette score for a range of number of cluster
    def elbow_with_silhouette_scores(self):
        silhouette_scores = []
        for i in range(2, 11):
            km = KMeans(
                n_clusters=i, init='k-means++',
                n_init=10, max_iter=100,
                tol=1e-04, random_state=0
            )
            km.fit(self.sentence_vectors)
            silhouette_scores.append(silhouette_score(self.sentence_vectors, km.labels_, metric='euclidean'))
            
        return silhouette_scores

    def plot_distortion(self):

        plt.plot(range(1, 11), self.elbow_with_distortions(), marker='o')
        plt.title("Distortion")
        plt.xlabel('Number of clusters', fontsize=15)
        plt.ylabel('Distortion', fontsize=15)
        plt.show()

    def plot_silhouette(self):
        plt.plot(range(2, 11), self.elbow_with_silhouette_scores(), marker='o')
        plt.title("Silhouette")
        plt.xlabel('Number of clusters', fontsize=15)
        plt.ylabel('silhouette score', fontsize=15)
        plt.show()

    def scatter_cluster(self):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.scatter(self.df['cluster'], self.df['sentence'], cmap='rainbow')

        # Add a title and axis labels
        ax1.set_title("Sentence Clusters")
        ax1.set_xlabel("Clusters")
        ax1.set_ylabel("Sentences")

        # ax1.set_yticklabels([])

        wordcloud = WordCloud(
        stopwords=STOPWORDS,
        height=1000,
        width=1000
        ).generate(self.text)

        ax2.imshow(wordcloud, interpolation="bilinear")
        ax2.axis('off')


        plt.show()

    def cloud_sentences(self):
        print()


if __name__ == "__main__":
    analysis = Analysis()
    analysis.cluster_datas()
    print(analysis.df)
    analysis.scatter_cluster()
