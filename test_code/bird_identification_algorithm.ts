import { BirdSpecies, BirdColor, BeakShape, TailShape, Habitat, BirdSize, BirdSearchParams } from './types';
//language=TypeScript, file extention should be .ts
export class BirdIdentifier {
  private readonly colorWeight = 0.35;
  private readonly beakWeight = 0.25;
  private readonly tailWeight = 0.15;
  private readonly sizeWeight = 0.15;
  private readonly habitatWeight = 0.10;

  /**
   * Identifies birds based on user observations
   * Returns matches sorted by confidence with detailed scoring
   */
  public identifyBirds(
    searchParams: BirdSearchParams,
    birdDatabase: BirdSpecies[],
    limit: number = 5
  ): {
    matches: Array<{
      bird: BirdSpecies;
      scores: {
        colorScore: number;
        beakScore: number;
        tailScore: number;
        sizeScore: number;
        habitatScore: number;
        totalScore: number;
      };
    }>;
  } {
    const matches = birdDatabase.map(bird => {
      const scores = this.calculateScores(searchParams, bird);
      return { bird, scores };
    });

    // Sort by total score and take top matches
    return {
      matches: matches
        .sort((a, b) => b.scores.totalScore - a.scores.totalScore)
        .slice(0, limit)
    };
  }

  private calculateScores(params: BirdSearchParams, bird: BirdSpecies) {
    const colorScore = this.calculateColorScore(params, bird);
    const beakScore = this.calculateBeakScore(params, bird);
    const tailScore = this.calculateTailScore(params, bird);
    const sizeScore = this.calculateSizeScore(params, bird);
    const habitatScore = this.calculateHabitatScore(params, bird);

    const totalScore = 
      (colorScore * this.colorWeight) +
      (beakScore * this.beakWeight) +
      (tailScore * this.tailWeight) +
      (sizeScore * this.sizeWeight) +
      (habitatScore * this.habitatWeight);

    return {
      colorScore,
      beakScore,
      tailScore,
      sizeScore,
      habitatScore,
      totalScore
    };
  }

  private calculateColorScore(params: BirdSearchParams, bird: BirdSpecies): number {
    if (!params.colors || params.colors.length === 0) return 1;

    // Combine all bird colors for comparison
    const birdColors = new Set([
      ...bird.plumageColors,
      ...bird.beakColors,
      ...bird.feetColors,
      ...bird.legColors
    ]);

    // Calculate matches and penalties
    let matches = 0;
    let falsePositives = 0;
    let falseNegatives = 0;

    // Count matching colors
    params.colors.forEach(color => {
      if (birdColors.has(color)) {
        matches++;
      } else {
        falsePositives++;
      }
    });

    // Count missing colors
    birdColors.forEach(color => {
      if (!params.colors.includes(color)) {
        falseNegatives++;
      }
    });

    // Calculate F1-score like metric
    const precision = matches / (matches + falsePositives);
    const recall = matches / (matches + falseNegatives);
    
    if (precision + recall === 0) return 0;
    return 2 * (precision * recall) / (precision + recall);
  }

  private calculateBeakScore(params: BirdSearchParams, bird: BirdSpecies): number {
    if (!params.beakShape || params.beakShape.length === 0) return 1;

    const matchCount = params.beakShape.filter(shape => 
      bird.beakShapes.includes(shape)
    ).length;

    // Consider it a full match if any of the beak shapes match
    return matchCount > 0 ? 1 : 0;
  }

  private calculateTailScore(params: BirdSearchParams, bird: BirdSpecies): number {
    if (!params.tailShape || params.tailShape.length === 0) return 1;

    const matchCount = params.tailShape.filter(shape => 
      bird.tailShapes.includes(shape)
    ).length;

    // Consider it a full match if any of the tail shapes match
    return matchCount > 0 ? 1 : 0;
  }

  private calculateSizeScore(params: BirdSearchParams, bird: BirdSpecies): number {
    if (!params.size || params.size.length === 0) return 1;

    // If exact size category matches
    if (params.size.includes(bird.size)) return 1;

    // Calculate partial score based on size difference
    const sizeOrder = [
      BirdSize.VERY_SMALL,
      BirdSize.SMALL,
      BirdSize.MEDIUM,
      BirdSize.LARGE,
      BirdSize.VERY_LARGE
    ];

    const birdSizeIndex = sizeOrder.indexOf(bird.size);
    const paramSizeIndexes = params.size.map(s => sizeOrder.indexOf(s));
    
    // Find closest size match
    const closestDistance = Math.min(
      ...paramSizeIndexes.map(i => Math.abs(i - birdSizeIndex))
    );

    // Score decreases with distance from actual size
    return Math.max(0, 1 - (closestDistance * 0.25));
  }

  private calculateHabitatScore(params: BirdSearchParams, bird: BirdSpecies): number {
    if (!params.habitat || params.habitat.length === 0) return 1;

    const matchCount = params.habitat.filter(habitat => 
      bird.habitats.includes(habitat)
    ).length;

    // Calculate partial score based on habitat matches
    return matchCount / params.habitat.length;
  }

  /**
   * Helper method to explain the identification results in child-friendly terms
   */
  public explainResults(scores: {
    colorScore: number;
    beakScore: number;
    tailScore: number;
    sizeScore: number;
    habitatScore: number;
    totalScore: number;
  }): string {
    const explanations = [];
    
    if (scores.colorScore > 0.8) {
      explanations.push("The colors match really well!");
    } else if (scores.colorScore > 0.5) {
      explanations.push("Some of the colors match.");
    }

    if (scores.beakScore > 0.8) {
      explanations.push("The beak shape is just right!");
    }

    if (scores.tailScore > 0.8) {
      explanations.push("The tail shape matches perfectly!");
    }

    if (scores.sizeScore > 0.8) {
      explanations.push("The size is exactly right!");
    } else if (scores.sizeScore > 0.5) {
      explanations.push("The size is pretty close.");
    }

    if (scores.habitatScore > 0.8) {
      explanations.push("And you found it in just the right place!");
    }

    if (explanations.length === 0) {
      return "I'm not quite sure about this bird. Can you tell me more about what you saw?";
    }

    return explanations.join(" ");
  }
}

// Example usage:
/*
const identifier = new BirdIdentifier();
const results = identifier.identifyBirds(
  {
    colors: [BirdColor.WHITE, BirdColor.GREY],
    beakShape: [BeakShape.LONG_THICK_CURVED],
    habitat: [Habitat.COAST]
  },
  birdDatabase
);

results.matches.forEach(match => {
  console.log(`${match.bird.commonName}: ${match.scores.totalScore * 100}% match`);
  console.log(identifier.explainResults(match.scores));
});
*/