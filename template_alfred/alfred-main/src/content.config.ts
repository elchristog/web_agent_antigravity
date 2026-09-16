import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

const helpcenter = defineCollection({
  loader: glob({ pattern: "**/*.(md|mdx)", base: "./src/content/helpcenter" }),
  schema: z.object({
    title: z.string(),
    intro: z.string(),
  }),
});

const changelog = defineCollection({
  loader: glob({ pattern: "**/*.(md|mdx)", base: "./src/content/changelog" }),
  schema: ({ image }) =>
    z.object({
      page: z.string(),
      description: z.string(),
      pubDate: z.date(),
      image: z.object({
        url: image(),
        alt: z.string(),
      }),
    }),
});

const infopages = defineCollection({
  loader: glob({ pattern: "**/*.(md|mdx)", base: "./src/content/infopages" }),
  schema: z.object({
    page: z.string(),
    pubDate: z.date(),
  }),
});

const integrations = defineCollection({
  loader: glob({ pattern: "**/*.(md|mdx)", base: "./src/content/integrations" }),
  schema: ({ image }) =>
    z.object({
      email: z.string(),
      integration: z.string(),
      description: z.string(),
      permissions: z.array(z.string()),
      details: z.array(
        z.object({
          title: z.string(),
          value: z.string(),
          url: z.optional(z.string()),
        })
      ),
      logo: z.object({
        url: image(),
        alt: z.string(),
      }),
      tags: z.array(z.string()),
    }),
});

const team = defineCollection({
  loader: glob({ pattern: "**/*.(md|mdx)", base: "./src/content/team" }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      role: z.string().optional(),
      bio: z.string().optional(),
      image: z.object({
        url: image(),
        alt: z.string(),
      }),
      socials: z
        .object({
          twitter: z.string().optional(),
          website: z.string().optional(),
          linkedin: z.string().optional(),
          email: z.string().optional(),
        })
        .optional(),
    }),
});

const postsCollection = defineCollection({
  loader: glob({ pattern: "**/*.(md|mdx)", base: "./src/content/posts" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      pubDate: z.date(),
      description: z.string(),
      team: z.string().optional(),
      image: z.object({
        url: z.union([image(), z.string()]),
        alt: z.string(),
      }),
      tags: z.array(z.string()),
    }),
});

export const collections = {
  posts: postsCollection,
};
